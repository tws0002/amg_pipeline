from shotgun_api3.shotgun import Shotgun
import sgtk
import re

AMG_SERVER_PATH = 'https://animagrad.shotgunstudio.com'
AMG_SCRIPT_USER = 'Toolkit'
AMG_SCRIPT_KEY  = '2062d7c5d64ad72552fb0e983bd25203a823580620410a56367ac491d325fc6f'


class SG(object):
    type = None
    def __init__(self, id, data=None):
        self.id = id
        self.sg = self.create_connection(AMG_SERVER_PATH, AMG_SCRIPT_USER, AMG_SCRIPT_KEY)
        self.data = None
        if self.type:
            if not data:
                self.data = self.sg.find_one(self.type ,[['id','is',id]], self.fields_for(self.type))
            else:
                self.data = data
        self.name = 'noname'

    def __repr__(self):
        return '%s "%s" (%s)' % (self.type, self.name, self.id)

    # create connections
    @staticmethod
    def create_connection(SERVER_PATH=None, SCRIPT_USER=None, SCRIPT_KEY=None):
        SERVER_PATH = SERVER_PATH or AMG_SERVER_PATH
        SCRIPT_USER = SCRIPT_USER or AMG_SCRIPT_USER
        SCRIPT_KEY  = SCRIPT_KEY or AMG_SCRIPT_KEY
        return  Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

    # query all
    def get_all_steps(self, filters = None, fields=None):
        filters = filters or []
        fields = fields or ['code',"entity_type"]
        return self.sg.find("Step", filters, fields)

    @staticmethod
    def get_all_projects():
        # filters = filters or []
        # fields = fields or ['name']
        # return self.sg.find('Project', filters, fields)
        sg = SG.create_connection()
        projects = sg.find('Project',[], sg.schema_field_read('Project').keys())
        return [SG_Project(id=x['id'], data=x) for x in projects]

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
        userList = cls.create_connection().find("HumanUser",filters,fields)
        return userList
    @classmethod
    def get_all_api_users(cls):
        fields = cls.fields_for('ApiUser')
        filters = []
        userList = cls.create_connection().find("ApiUser",filters,fields)
        return userList
    @classmethod
    def get_all_client_users(cls):
        fields = cls.fields_for('ClientUser')
        filters = []
        userList = cls.create_connection().find("ClientUser",filters,fields)
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
        return cls.create_connection().schema_field_read(type).keys()

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

class SG_Project(SG):
    type='Project'
    def __init__(self, id, data=None):
        super(SG_Project, self).__init__(id, data=data)
        # shortcuts
        self.name = self.data['name']
        # variables
        self._sequences = None
        self._shots = None

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

    @classmethod
    def named(cls, name):
        projects = SG.get_all_projects()
        for prj in projects:
            if prj.name == name:
                return prj

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


