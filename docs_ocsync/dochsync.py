# -*- coding: utf-8 -*-
from openerp import models, fields, api
from conf import settings
import os, sys
import hashlib

#import pydevd
import re

'''
Modelo que crea la tarea planificada de sincronizacion de Owncloud con Odoo
'''
class sync_server_action(models.Model):
    _name = "sync.server.action"
     
    @api.model
    def create_server_action(self):
        cronmodel = self.env['ir.cron']
        crontask = cronmodel.search([('name','=','Owncloud->Odoo')])
        if not crontask:
            args = {'name':'Owncloud->Odoo', 'interval_number':int(settings.SYNC_ACTION_MINUTES),
                    'interval_type':'minutes', 'model':'ir.attachment',
                    'function':'periodical_sync_files', 'active':True, 'numbercall':-1}
            cronmodel.create(args)

sync_server_action()

'''
Modelo que exitende ir.attachment para introducir la sincronizacion
con Owncloud en ambos sentidos Odoo->OC y OC->Odoo
'''
class ir_attachment(models.Model):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'
    
    '''
    Sobreescribe el metodo create de ir.attachment
    Cada vez que se cree un registro obtiene el path en formato humano del directorio en el que se va 
    a almacenar el archivo y que estara conectado a un sistema de almacenamiento cloud, como Owncloud.
    Una vez obtenido el path humano se mueve el archivo para que se referencie con ese nombre y se
    convierte el nombre alien interno del archivo generado por Odoo a un enlace simbolico al archivo
    movido. De este modo el sistema de gestion de documentos de Odoo almacenara nombres alien que
    correspoden a enlaces simbolicos que apuntan a archivos con nombre humano
    '''
    @api.model
    def create(self, values):
        #pydevd.settrace('10.0.3.1')
        attach = super(ir_attachment, self).create(values)        
        if 'syncori' in self.env.context and 'syncdest' in self.env.context:
            ori = self.env.context['syncori']
            dest = self.env.context['syncdest']
            if os.path.exists(dest):
                os.remove(dest)
            #Creamos el directorio padre del enlace alien
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))                                                                                   
            #Creamos el enlace simbolico con nombre alien  
            os.symlink(ori, dest)            
        else:
            pathalien, pathhuman = self._get_filespaths()
            docdirmodel = self.env['document.directory']
            #Datos del modelo asociado al ir.attachment
            resmodel = attach.res_model
            resid = attach.res_id
            if resmodel and resid:
                #Accedemos al modelo asociado segun la informacion anterior
                irmodel = self.env['ir.model']
                elmodel = irmodel.search([('model', '=', resmodel)], limit=1)
                mmodel = self.env[elmodel.model]
                res = mmodel.search([('id','=',resid)])
                #Busco directorios para ese modelo
                dirs = docdirmodel.search([('ressource_type_id.id', '=', elmodel.id)])
                for dir in dirs:
                    #Path absoluto al directorio en formato humano
                    #pydevd.settrace('10.0.3.1')
                    path = pathhuman + '/' + dir.get_recursive_path_directory(res)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    #Aplicaremos dominios para restriccion por el domain del directory y el resid
                    ddomain = dir.domain
                    domain = eval(str(ddomain))
                    #restringimos por el id del registro y el domain del directory
                    if not domain:
                        domain = []                            
                    domain.append(('id', '=', resid))
                    reg = mmodel.search(domain)
                    '''
                    Si encontramos un registro movemos el archivo original al directorio de nombres
                    humanos de OC, a continuación creamos el enlace simbolico desde la ruta al archivo
                    almacenada en Odoo que apunta al archivo en OC
                    '''                    
                    if reg:                            
                        if not os.path.exists(path): 
                            os.makedirs(path)
                        '''
                        El nombre del adjunto llevara un identificador del registro asociado, bien en el
                        nombre del archivo, o bien en un directorio creado especificamente para cada registro.
                        Esta opcion se indica en el campo gen_id_filename de document.directory
                        '''
                        field_id = ""
                        if dir.gen_id_filename:
                            if dir.id_owncloud:       
                                field_id = dir.id_owncloud
                            else:
                                field_id = 'id'                            
                        '''
                        En la opcion de generar el id de registro en el nombre del archivo,
                        si hay caracteres / en el identificador, estos se eliminan ya que no son caracteres
                        validos para nombres de archivo
                        '''
                        if field_id:
                            fid = eval('reg.' + field_id)
                            if not type(fid) is unicode:
                                fid = unicode(fid)
                            fid = fid.replace('/', '')
                            human_fname = path + '/' + fid + '_' + attach.name
                        else:
                            human_fname = path + '/' + attach.name      
                        if not os.path.exists(human_fname):
                            #Muevo el archivo al directorio de nombres humanos
                            os.rename(pathalien + '/' + attach.store_fname, human_fname)
                            #Actualizamos marca horaria del archivo para detectar cambios en la sincronizacion
                            _change_path_utime(pathhuman, path)
                            #Convierto el nombre del archivo alien de Odoo a un enlace al archivo con nombre humano
                            os.symlink(human_fname, pathalien + '/' + attach.store_fname)                            
        return attach
                    
    '''
    Sobreescribe el metodo unlink de ir.attachment
    Cuando se elimine un registro se eliminara tambien el archivo con nombre humano al que
    el registro borrado apuntaba mediante un enlace simbolico con nombre alien recogido en el 
    campo store_fname
    '''
    @api.multi
    def unlink(self):
        try:            
            if not 'nodel' in self.env.context:
                pathalien, pathhuman = self._get_filespaths()
                docdirmodel = self.env['document.directory']
                resmodel = self.res_model
                resid = self.res_id
                #pydevd.settrace('10.0.3.1')
                if resmodel and resid:
                    irmodel = self.env['ir.model']
                    elmodel = irmodel.search([('model', '=', resmodel)], limit=1)
                    mmodel = self.env[elmodel.model]
                    res = mmodel.search([('id','=',resid)])         
                    #Busco directorios para ese modelo
                    dirs = docdirmodel.search([('ressource_type_id', '=', elmodel.id)])
                    #Recorro los directorios del modelo asociado al ir.attachment
                    for dir in dirs:
                        #Path absoluto al directorio en formato humano
                        path = pathhuman + '/' + dir.get_recursive_path_directory(res)
                        #Busco en ese path el archivo al que apuntaba el ir.attachment borrado
                        for root, dirs, files in os.walk(path):
                            for name in files:
                                #pydevd.settrace('10.0.3.1')
                                filepath = os.path.join(root, name)
                                #Borro el archivo asociado al enlace simbolico alien de Odoo y el enlace
                                #pydevd.settrace('10.0.3.1')
                                linkfile = os.path.realpath(pathalien + '/' + self.store_fname)
                                if filepath in linkfile:
                                    #Borramos el archivo del path de OC
                                    os.remove(filepath)
                                    #Actualizamos marca horaria del archivo para detectar cambios en la sincronizacion
                                    _change_path_utime(pathhuman, os.path.dirname(filepath))
                                    #Borramos el enlace simbolico
                                    os.remove(pathalien + '/' + self.store_fname)
                                    break
        except:
            pass
        #Independientemente de lo que ocurra en el codigo anterior debe de llamarse al unlink del padre
        return super(ir_attachment, self).unlink()
    
    @api.cr_uid
    def periodical_sync_files(self, cr, uid, ids=None, context=None):        
        docdirmodel = self.pool.get('document.directory')
        pathalien, pathhuman = self._get_filespaths_oldapi(cr, uid)
        #Recorremos los directorios de recursos                     
        dirswithmodels = docdirmodel.search(cr, uid, ['!',('ressource_type_id','=',None)], context=context)
        for dwm in dirswithmodels:
            #Extremos el modelo del directorio de recurso evaluado
            dd = docdirmodel.browse(cr, uid, dwm)
            model = dd.ressource_type_id                       
            #Construyo el path humano para el directorio evaluado
            #pydevd.settrace('10.0.3.1')           
            dirpath = pathhuman + '/' + dd.get_recursive_path_directory()           
            #Tomamos los ir.attachment para el modelo evaluado
            attachs = self.search(cr, uid, [('res_model', '=', model.model)], context=context)
            #Lista con path humanos de ir.attachment del modelo
            pathsumanlist = [os.path.realpath(pathalien + '/' + self.browse(cr, uid, att).store_fname) for att in attachs]
            #Borrado de los ir.attachment que no apuntan a ningun archivo existente porque este se ha borrado            
            attsdel = []
            for att in attachs:
                if not os.path.exists(os.path.realpath(pathalien + '/' + self.browse(cr, uid, att).store_fname)):
                    attsdel.append(att)
            #pydevd.settrace('10.0.3.1')            
            for attdel in attsdel:
                context = dict(context or {})                        
                context.update({'nodel':True})                
                self.unlink(cr, uid, attdel, context=context)                
            #Lista de ir.attachment a crear
            files2createlist = []
            #Recorremos el path humano del directorio en busca de archivos no enlazados desde los attachs
            for root, dirs, files in os.walk(dirpath):
                for file in files:
                    if not os.path.join(root, file) in pathsumanlist:
                        files2createlist.append(os.path.join(root, file))
            #Para cada file de la lista hay que crear el ir.attachment y establecer el enlace simbolico al archivo
            #pydevd.settrace('10.0.3.1') 
            for f2c in files2createlist:
                sha = _sha1sum(f2c)
                '''
                Nombre alien calculando el sha1 del archivo
                Se genera un directorio con los 2 primeros caracteres del sha1
                Dentro de ese directorio se ubica el archivo con el nombre sha1 obtenido
                '''
                fname = sha[:2] + '/' + sha
                '''
                El identificador del registro se obtiene del nombre del archivo, concretamente de la parte
                del nombre que esta antes del primer caracter _ y correspondera con el valor del campo 
                identificador id_owncloud definido en document.directory
                '''                              
                resmodel = self.pool.get(model.model)
                resname = ""
                #pydevd.settrace('10.0.3.1')  
                if dd.gen_id_filename:
                    #Si el nombre del registro forma parte del nombre del archivo
                    resname = os.path.basename(f2c).split("_")[0]                  
                else:
                    #pydevd.settrace('10.0.3.1')
                    #Sino, buscamos en la ruta de directorios                    
                    peaces = dd.path_owncloud.split("/")
                    n = len([d for d in peaces if d])
                    #A partir de la parte final de la ruta que corresponde al identificador de registro
                    resname = os.path.dirname(f2c).split(dirpath)[1]                   
                    resname = resname.split("/", n+1)
                    resname = resname[len(resname)-1]
                #Si se especifica un campo de identificacion del registro en document.directory
                if dd.id_owncloud:
                    field = dd.id_owncloud
                #Sino usamos el id del registro
                else:
                    field = 'id'
                if resname.isdigit() and resmodel._columns[field]._type in ('float','integer'):
                    ress = resmodel.search(cr, uid, [(field, '=', resname)], context=context)
                elif not resmodel._columns[field]._type in ('float','integer'):
                    ress = resmodel.search(cr, uid, [(field, 'like', resname)], context=context)                                        
                
                '''
                Puede darse el caso de que el number o el name contengan nombres con /
                en cuyo caso hay que comprobar que la ruta correspondiente generada
                este contenida en el path absoluto del directorio procesado (root)
                '''    
                #ress = resmodel.search(cr, uid, [(field, 'like', resname)], context=context)                             
                for r in ress:
                    rr = resmodel.browse(cr, uid, r)
                field = ''
                 
                if 'rr' in locals():                                                                         
                    #pydevd.settrace('10.0.3.1')
                    ori = os.path.abspath(f2c)
                    dest = pathalien + '/' + fname
                    #Crea el ir.attachment invocando a create, lo que creara en link simbolico automaticamente
                    if os.path.exists(ori):
                        #pydevd.settrace('10.0.3.1')
                        #Creo el ir.attachment
                        attname = os.path.basename(ori)
                        if dd.gen_id_filename:
                            attnamep = attname.split("_", 1)
                            if len(attnamep) > 1:
                                attname = attnamep[1]
                        context = dict(context or {})                        
                        context.update({'syncori':ori, 'syncdest':dest}) 
                        attach = self.create(cr, uid, {'res_model':model.model, 'name':attname, 'type':'binary',
                                                       'res_name':resname, 'res_id':rr.id, 'store_fname':fname}, context=context) 
                        
    #Obtiene los paths a los directorios alien y humano en sintaxis de la old api    
    def _get_filespaths_oldapi(self, cr, uid, context=None):
        irconfigparmodel = self.pool.get('ir.config_parameter')
        #Buscamos si esta definido un parametro del sistema para el path al filestore
        pfilespath = irconfigparmodel.search(cr, uid, [('key', '=', 'path.filestore')], context=context)
        if pfilespath: 
            filespath = irconfigparmodel. browse(cr, uid, pfilespath).value
        else:           
            filespath = settings.ODOO_FILESTORE            
            irconfigparmodel.create(cr, uid, {'key':'path.filestore', 'value':filespath})
        return filespath + '/' + cr.dbname, filespath + '/' + cr.dbname + '/human'
    
    #Obtiene los paths a los directorios alien y humano
    def _get_filespaths(self):
        irconfigparmodel = self.env['ir.config_parameter']        
        #Buscamos si esta definido un parametro del sistema para el path al filestore
        pfilespath = irconfigparmodel.search([('key', '=', 'path.filestore')])
        if pfilespath:
            filespath = pfilespath.value
        else:                       
            filespath = settings.ODOO_FILESTORE            
            irconfigparmodel.create({'key':'path.filestore', 'value':filespath})
        return filespath + '/' + self.env.cr.dbname, filespath + '/' + self.env.cr.dbname + '/human'       

    @api.multi
    def test_filestore_sync(self):
        pass

ir_attachment()

'''
Modelo que extiende document.directory para meter las rutas
personalizadas de Owncloud
'''
class document_directory(models.Model):
    _name = 'document.directory'
    _inherit = 'document.directory'

    '''
    Construye el path del directorio teniendo en cuenta el anidamiento de los directorios padres
    '''
    def get_recursive_path_directory(self, res=None):
        '''
        Obtenemos la parte generica de la ruta del directorio
        '''
        pathdes = ""
        diraux = self
        while diraux.parent_id:
            #Insertamos el nombre del directorio delante, la ruta va de abajo arriba
            pathdes = ''.join(diraux.name + '/' + pathdes)
            diraux = diraux.parent_id
            
        if not pathdes:
            pathdes = "/"
                 
        '''
        Si se especifica un path relativo Owncloud se utiliza ese
        para agregar a la ruta
        '''      
        #pathoc = pathdes[:-1] + '/' + self._process_path_owncloud(res)
        pathoc = self._process_path_owncloud(res)
        if self.path_owncloud:
            pathdes = pathoc        
        
        #Limpiamos los / del principio y el final
        if pathdes:
            if list(pathdes)[0] == "/":
                pathdes = pathdes.replace('/', '', 1)
            if list(pathdes)[len(pathdes)-1] == "/":
                pathdes = pathdes[:-1]
        
        return pathdes
    
    def _process_path_owncloud(self, res):
        #pydevd.settrace('10.0.3.1')
        path = ""       
        if self.path_owncloud:
            path = self.path_owncloud            
            if res:
                p = re.compile('(%[\w|.|_]+%)')
                replaces = p.findall(path)
                for r in replaces:               
                    field = r[1:len(r)-1]                    
                    value = eval('res.' + field)
                    if not type(value) is unicode:
                        value=unicode(value)
                    path = path.replace(r, value)
                '''
                Si no esta habilitada la opcion en el document.directory de agregar el 
                identificativo para cada registro en el nombre del archivo, se crea un directorio
                concatenando el valor del campo del registro indicado a la ruta
                '''
                if not self.gen_id_filename:
                    dir_id_name = ''
                    if self.id_owncloud:
                        dir_id_name = unicode(eval('res.' + self.id_owncloud))
                    else:
                        dir_id_name = unicode(eval('res.id'))
                    #Quitamos las / del nombre del id del registro para evitar subdirectorios                    
                    #pydevd.settrace('10.0.3.1')                    
                    dir_id_name = dir_id_name.replace('/', '')
                    if path and path[0] == '/':
                        path = path[1:]
                    path = path + '/' + dir_id_name 
                        
            #Sino hay res se corta la ruta a partir del primer %
            else:
                path = path.split('%')[0]               
                
            if path and path[0] == '/':
                return path[1:]            
        
        return path
         
    
    #fields
    path_owncloud = fields.Char('Path Relativo Owncloud', size=200,
                                help="Estructura de directorios organizativa a partir del directorio principal. " +
                                "Permite utilizar campos del modelo encerrados entre caracteres %")
    id_owncloud = fields.Char('Campo identificativo de Documentos', size=100,
                              help="Campo que permite identificar un registro y asociar los documentos con él. " +
                              "Sino se especifica nada utiliza el id del registro")
    gen_id_filename = fields.Boolean('Identificativo en nombre archivo', default=True,
                                     help="Identficador de registro en nombre de archivo. Sino se selecciona " +
                                     "crea un directorio para cada registro según el Campo identificativo")    

document_directory()

'''
Cambia las marcas de tiempo de los directorios en el path topath desde el path frompath
Esto es necesario para la sincronizacion con el cliente de escritorio de Owncloud
'''
def _change_path_utime(frompath, topath):
    #pydevd.settrace('10.0.3.1')
    while frompath in topath:
        os.utime(topath, None)
        topath = os.path.dirname(topath)


'''
Calcula el sha1 del archivo pasado codificado en hexadecimal
'''
def _sha1sum(filename):    
    f = open(filename, mode='r')
    d = hashlib.sha1()    
    try:
        for buf in f.read(65536):            
            d.update(buf)   
    except:
        e = sys.exc_info()[0]        
    digest = d.hexdigest()
    return digest