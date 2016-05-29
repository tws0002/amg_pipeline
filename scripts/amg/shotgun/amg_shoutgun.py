from amg.packages.shotgun_api3.shotgun import Shotgun
try:
    from amg.packages import yaml
except:
    import yaml
try:
    import sgtk
    from tank.util import shotgun
except:
    shotgun = None
import re, os, json, datetime, time
import amg_config

AMG_SERVER_PATH = amg_config.conf.get('server_path','')
AMG_SCRIPT_USER = amg_config.conf.get('script_user','')
AMG_SCRIPT_KEY  = amg_config.conf.get('script_key','')
project_meta_file = 'amg_project'

global cache
cache = {}


class SG(object):
    type = None
    def __init__(self, id, data=None):
        self.id = id
        self.__sg = None
        self.data = None
        if self.type:
            if not data:
                self.data = self.sg.find_one(self.type ,[['id','is',id]], self.fields_for(self.type))
            else:
                self.data = data
        self.name = None

    def __repr__(self):
        return '%s "%s" (%s)' % (self.type, self.name, self.id)

    @property
    def sg(self):
        if not self. __sg:
            self.__sg = self.create_connection(AMG_SERVER_PATH, AMG_SCRIPT_USER, AMG_SCRIPT_KEY)
        return self. __sg

    @sg.setter
    def sg(self, v):
        raise Exception('This variable read only')

    @staticmethod
    def no_shotgun_message():
        print 'Shotgun not loaded'

    # create connections
    @staticmethod
    def create_connection(SERVER_PATH=None, SCRIPT_USER=None, SCRIPT_KEY=None):
        if not shotgun:
            SG.no_shotgun_message()
            return
        SERVER_PATH = SERVER_PATH or AMG_SERVER_PATH
        SCRIPT_USER = SCRIPT_USER or AMG_SCRIPT_USER
        SCRIPT_KEY  = SCRIPT_KEY or AMG_SCRIPT_KEY
        return  Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

    # query all
    def get_all_steps(self, filters = None, fields=None):
        if not shotgun:
            SG.no_shotgun_message()
            return
        filters = filters or []
        fields = fields or ['code',"entity_type"]
        return self.sg.find("Step", filters, fields)

    @staticmethod
    def get_all_projects(forse=False):
        global cache
        if not forse:
            if cache.get('list_projects'):
                return cache.get('list_projects')
        else:
            projects = SG.update_meta_projects_from_sever(False)
            cache['list_projects'] = projects
            return projects
        # from meta
        projects = SG.get_projects_meta()
        if projects:
            SG.update_meta_projects_from_sever(True)
            cache['list_projects'] = projects
            return projects
        # from server
        if not forse:
            return SG.get_all_projects(True)

    @staticmethod
    def update_meta_projects_from_sever(in_thread=False):
        if in_thread:
            return [] # todo: update project in separated process
        sg = SG.create_connection()
        if not sg:
            return
        projects = sg.find('Project',[], sg.schema_field_read('Project').keys())
        projects = [SG_Project(id=x['id'], data=x) for x in projects]
        SG.save_projects_meta(projects)
        return projects

    @staticmethod
    def save_projects_meta(projects):
        for p in projects:
            prj_path = p.path()
            if not prj_path or not os.path.exists(prj_path):continue
            meta_path = os.path.join(prj_path, project_meta_file).replace('\\','/')
            meta = dict(
                tank_name=p.data['tank_name'],
                cached_display_name=p.data['cached_display_name'],
                created_by=p.data['created_by'],
                id=p.data['id'],
                start_date=p.data['start_date'],
                sg_description=p.data['sg_description'],
                end_date=p.data['end_date'],
                archived=p.data['archived'],
                name=p.data['name'],
                created_at=time.mktime(p.data['created_at'].timetuple()),
                sg_start=p.data['sg_start'],
                is_template=p.data['is_template'],
                sg_fps=p.data['sg_fps'],
                tag_list=p.data['tag_list']
            )
            json.dump(meta, open(meta_path, 'w'), indent=2)

    @staticmethod
    def get_projects_meta():
        projects = []
        prj_path = amg_config.conf.get('projects_path')
        if not prj_path:
            return []
        for prj in os.listdir(prj_path):
            meta = os.path.join(prj_path, prj, project_meta_file)
            if os.path.exists(meta):
                data = json.load(open(meta))
                p = SG_Project(data['id'], data)
                projects.append(p)
        return projects

    @staticmethod
    def current_context():
        try:
            return sgtk.platform.current_engine().context
        except:
            return

    @classmethod
    def get_all_users(cls):
        fields = cls.fields_for('HumanUser')
        filters = []
        sg = cls.create_connection()
        if not sg:
            return
        userList = sg.find("HumanUser",filters,fields)
        return userList
    @classmethod
    def get_all_api_users(cls):
        fields = cls.fields_for('ApiUser')
        filters = []
        sg = cls.create_connection()
        if not sg:
            return
        userList =  sg.find("ApiUser",filters,fields)
        return userList
    @classmethod
    def get_all_client_users(cls):
        fields = cls.fields_for('ClientUser')
        filters = []
        sg = cls.create_connection()
        if not sg:
            return
        userList = sg.find("ClientUser",filters,fields)
        return userList

    @classmethod
    def fields_for(cls, type):
        """
        "ActionMenuItem", "ApiUser", "AppWelcomeUserConnection", "Asset", "AssetAssetConnection", "AssetBlendshapeConnection",
         "AssetElementConnection", "AssetMocapTakeConnection", "AssetSceneConnection", "AssetSequenceConnection", "AssetShootDayConnection",
         "AssetShotConnection", "Attachment", "BannerUserConnection", "Booking", "CameraMocapTakeConnection", "ClientUser",
         "CustomEntity01", "CutVersionConnection", "Department", "ElementShotConnection", "EventLogEntry", "FilesystemLocation",
         "Group", "GroupUserConnection", "HumanUser", "Icon", "LaunchSceneConnection", "LaunchShotConnection", "LocalStorage",
         "MocapTakeRangeShotConnection", "Note", "Page", "PageHit", "PageSetting", "PerformerMocapTakeConnection", "PerformerRoutineConnection",
         "PerformerShootDayConnection", "PermissionRuleSet", "Phase", "PhysicalAssetMocapTakeConnection", "PipelineConfiguration",
         "Playlist", "PlaylistShare", "PlaylistVersionConnection", "Project", "ProjectUserConnection", "PublishedFile",
         "PublishedFileDependency", "PublishedFileType", "ReleaseTicketConnection", "Reply", "RevisionRevisionConnection",
         "RevisionTicketConnection", "RvLicense", "Sequence", "ShootDaySceneConnection", "Shot", "ShotShotConnection", "Status",
         "Step", "Task", "TaskDependency", "TaskTemplate", "TicketTicketConnection", "TimeLog", "Version"
         """
        sg = cls.create_connection()
        if not sg:
            return
        return sg.schema_field_read(type).keys()

    def clear_cache(self):
        for atr in self.__dict__.keys():
            if re.match(r"^_{1}[a-zA-Z0-9]+[a-zA-Z0-9_]*$",atr):
                setattr(self, atr, None)
    @classmethod
    def quick_create_note(cls, user, subject, content, entity, project, sg=None, notify=False):
        """
            user: Shotgun user. Example: {'type':"HumanUser",'id':00}
            subject: Subject of note
            content: Text of note
            entity: Shot, Asset, Task ... object or list objects. Example: {'type': 'Shot', 'id': 1234}
            sg: Ready shotgun connection if need
            notify: Notify followers by Email
        """
        if not isinstance(entity, list):
            entity = [entity]
        data={
            'cached_display_name':"%s's note" % user['name'],
            'subject':subject,
            'created_by':user,
            'content':content,
            'sg_status_list':'opn',
            'updated_by':user,
            'user':user,
            'suppress_email_notif':True,
            'note_links':[entity],
            'project':{'type':'Project','id':78}}
        sg = sg or cls.create_connection()
        note = sg.create("Note",data)
        return note

    # @staticmethod
    # def pipeline_root(project):
    #     import amg_config
    #
    #     return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sgtk.__file__)))))
    @staticmethod
    def studio_url():
        if not shotgun:
            return
        return shotgun.get_associated_sg_base_url()

    @classmethod
    def define(cls, path):
        pass
# SG.update_meta_projects_from_sever(True)


class SG_Project(SG):
    type='Project'
    def __init__(self, id, data=None):
        super(SG_Project, self).__init__(id, data=data)
        # shortcuts
        self.name = self.data['name']
        self.code = data['tank_name']
        # variables
        self._sequences = None
        self._shots = None
        self._tank_path = None
        meta_path = os.path.join(self.path(), project_meta_file).replace('\\','/')
        if not os.path.exists(meta_path):
            self.meta = None
        else:
            self.meta = dict(
                path=meta_path,
                data=json.load(open(meta_path))
            )

    def shots(self):
        # filters = [['project','is',{'type':'Project','id':self.id}]]
        # return self.sg.find('Shot', filters, ['name'])
        if not self._shots:
            filters = [['project','is',{'type':'Project','id':self.id}]]
            shots = self.sg.find('Shot', filters, self.fields_for('Shot'))
            self._shots = [SG_Shot(x['id'], data=x) for x in shots]
        return self._shots

    def sequences(self):
        if not self._sequences:
            filters = [['project','is',{'id': self.id, 'type': 'Project'}]]
            sq = self.sg.find(SG_Sequence.type, filters, self.fields_for(SG_Sequence.type))
            self._sequences = [SG_Sequence(shot['id'], data=shot) for shot in sq]
        return self._sequences

    def sequence(self, name=None, id=None):
        if not any([name, id]):
            raise Exception('Set name or id of shot')
        sq = self.sequences()
        if name:
            for s in sq:
                if s.name == name:
                    s._project = self
                    return s
        else:
            for s in sq:
                if s.id == id:
                    s._project = self
                    return s

    def path(self):
        if not self.data['tank_name']:
            return
        path = os.path.join(amg_config.conf['projects_path'], self.data['tank_name']).replace('\\','/')
        if os.path.exists(path):
            return path

    def tank_path(self):
        from tank import pipelineconfig_factory
        configs = pipelineconfig_factory._get_pipeline_configs()
        if self._tank_path:
            return self._tank_path
        for c in configs['pipeline_configurations']:
            if c['project.Project.tank_name'] == self.code:
                for k_path in ('windows_path','linux_path','mac_path'):
                    if os.path.exists(c[k_path]):
                        self._tank_path = c[k_path].replace('\\','/')
                        return self._tank_path

    @classmethod
    def named(cls, name, force=False, second=False):
        projects = SG.get_all_projects(force)
        for prj in projects:
            if prj.name == name or prj.data['tank_name'] == name:
                return prj
        if not second:
            return cls.named(name, True, True)
        else:
            return

    @classmethod
    def from_path(cls, path):
        if not os.path.exists(path):
            return
        if os.path.isfile(path):
            path = os.path.dirname(path)
        path_elem = path.replace('\\','/').split('/')
        while path_elem:
            meta = '/'.join(path_elem+[project_meta_file])
            if os.path.exists(meta):
                data = json.load(open(meta))
                name = data.get('tank_name')
                if not name:
                    return
                else:
                    prj = SG_Project(data['id'], data)
                    return prj
            else:
                path_elem.pop(-1)




    def software_paths(self):
        tank_path = self.tank_path()
        if not tank_path:
            print('Tank path not found')
            return
        paths = '/'.join([tank_path,'config/env/includes/paths.yml'])
        if os.path.exists(paths):
            try:
                paths = yaml.load(open(paths))
                return paths
            except:
                print 'Error parse'
                return {}
        else:
            print 'paths.yml not found %s' % paths
            return {}

    def app_versions(self, app):
        paths = '/'.join([self.tank_path(),'config/env/includes/app_launchers.yml'])
        if os.path.exists(paths):
            try:
                data = yaml.load(open(paths))
            except:
                return
            if 'launch_'+app in data:
                return data.get('launch_'+app).get('versions')
        else:
            return

    def get_app_bin(self, app, version=None, system=None):
        """
        maya or mayapy
        houdini or python
        nuke or nython
        mary or mython
        motionbuilder
        3dsmax
        photoshop
        hiero
        softimage
        rv
        """
        global cache
        if cache.get('project_aps'):
            if self.code in cache.get('project_aps'):
                if app in cache.get('project_aps').get(self.code):
                    return cache.get('project_aps').get(self.code).get(app)
        system = system or os.name
        result_app = pipeline_app = app
        binary_names = dict(
            hython=('houdini', 'hython'),
            mayapy=('maya','mayapy'),
            nython=('nuke','python'),
        )
        if pipeline_app in binary_names:
            result_app = binary_names[pipeline_app][1]
            pipeline_app = binary_names[pipeline_app][0]

        suff = {'nt':['windows', 'win'],'posix':['linux'],'os2': ['mac']}.get(system)
        if suff:
            path = [x for x in [self.software_paths().get('_'.join([pipeline_app, suf])) for suf in suff] if x]
            if not path:
                print 'Not found'
                return
            path = path[0]
            if not pipeline_app == result_app:
                dir = os.path.dirname(path)
                name, ext = os.path.splitext(os.path.basename(path))
                path = '/'.join([dir,result_app+ext])

            if '{version}' in path:
                versions = self.app_versions(pipeline_app)
                if not versions:
                    raise Exception('Version list not found in config')
                if version:
                    if not version in versions:
                        raise Exception('Requested version not found: %s (%s)' % (version, versions))
                    path = path.replace('{version}', str(version))
                else:
                    version = sorted(versions)[-1]
                    path = path.replace('{version}', str(version))
            path = path.replace('\\','/')
            # if not os.path.exists(path):
            #     print '>>> WARNING: File not exists on this machine'
            if cache.get('project_aps'):
                if cache['project_aps'].get(self.code):
                    cache['project_aps'][self.code][app] = path
                else:
                    cache['project_aps'][self.code] = {app: path}
            else:
                cache['project_aps'] = {self.code:{app: path}}
            return path



class SG_Sequence(SG):
    type='Sequence'
    def __init__(self, id, data=None):
        super(SG_Sequence, self).__init__(id, data)
        # shortcuts
        self.name = self.data['code']
        self._shots = None
        self._project = None

    def __repr__(self):
        return '%s "%s/%s" (%s)' % (self.type, self.data['project']['name'], self.name, self.id)

    def project(self):
        if not self._project:
            self._project = SG_Project(id=self.data['project']['id'])
        return self._project

    def shots(self):
        filters = [['sg_sequence','is',{'id': self.id, 'type': 'Sequence'}]]
        shots = self.sg.find('Shot', filters, self.fields_for('Shot'))
        if not self._shots:
            self._shots = [SG_Shot(id=shot['id'], data=shot) for shot in shots]
        return self._shots

    def shot(self, name=None, id=None):
        if not name and not id:
            raise Exception('Set name or id of shot')
        shots = self.shots()
        if name:
            for s in shots:
                if s.name == name:
                    s._sequence = self
                    return s
        else:
            for s in shots:
                if s.id == id:
                    s._sequence = self
                    return s


class SG_Shot(SG):
    type = 'Shot'
    def __init__(self, id, data=None):
        super(SG_Shot, self).__init__(id, data)
        self.name = self.data['code']
        self._sequence = None
        self._project = None

    def project(self):
        if not self._project:
            self._project = SG_Project(id=self.data['project']['id'])
        return self._project

    def sequence(self):
        if not self._sequence:
            self._sequence = SG_Sequence(self.data['sg_sequence']['id'])
        return self._sequence

    def __repr__(self):
        return '%s "%s/%s/%s" (%s)' % (self.type, self.data['project']['name'], self.data['sg_sequence']['name'], self.name, self.id)


class SG_Asset(SG):
    type = 'Asset'
    def __init__(self, id, data=None):
        super(SG_Asset, self).__init__(id, data)


class SG_Task(SG):
    type = 'Task'
    def __init__(self, id, data=None):
        super(SG_Task, self).__init__(id, data)


class SG_Afanasy(object):
    def __init__(self):
        super(SG_Afanasy, self).__init__()


if __name__ == '__main__':
    print 'TODO: update projects'