from jiuchai.utils import utils
class vote:

    def __init__(self):
        self.sender = []
        self.proposla = []
        self.participant = []
        self.participant_number = 0
        self.vote_number = 0
        self.vote_participant = []
        self.oppose_number = 0
        self.oppose_participant = []
        self.current_participant =0
        self.all_amount =0
        self.flag =False
        self.project = ''


    def send_proposal(self,sender,proposal,participant_number,project):
        #调用此函数需要传入四个变量，提议的发起人，提议内容，参与人数以及所提议项目的id
        self.sender.append(sender)
        self.proposla.append(proposal)
        self.participant_number = participant_number
        self.all_amount =count_project_amount(project)
        self.project = project

    def vote_proposal(self,participant):
        #该函数用来统计支持者的名单，使用时需要传入支持者的名称
        self.participant.append(participant)
        self.vote_participant.append(participant)
        self.vote_number =self.vote_number +1
        self.current_participant = self.current_participant +1
        #当检测到投票人数过半，启动判断部分，反对部分同理。
        if self.current_participant == self.participant_number:
            judge_number()


    def oppose_proposal(self,participant):
        #该函数用来统计反对者的名单,使用时需要传入反对者的名称
        self.participant.append(participant)
        self.oppose_participant.append(participant)
        self.oppose_number = self.oppose_number +1
        self.current_participant = self.current_participant + 1
        if self.current_participant == self.participant_number:
            judge_number()

    def judege_number(self):
        if self.vote_number > self.participant_number/2:
            judge_weight(self.vote_participant,self.project)
        elif self.oppose_number > self.participant_number/2:
            judge_weight(self.oppose_participant,self.project)
        elif self.oppose_number == self.vote_number:
            return '支持方与反对方票数相等'

    def judge_weight(self,participant,cid):
        for participant in participant:
            current_amount = count_somebody_amount(participant, cid)
            if current_amount > self.all_amount /2:
                return self.flag == True
            else:
                return  self.flag == False

