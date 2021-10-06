
class Room:
    room_states = ["Clean", "Dirty"]
    room_names = ['A', 'B']

    def __init__(self, loc, name):
        self.state = None  # random.choice(Room.room_states)
        self.loc = loc
        self.name = name

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_name(self):
        return self.name


class VaccuumEnvironment:

    #  (percept, initial location of agent) : [Action, final location]

    __scoring_LUT = {('A', "Clean", 'B', "Clean", 'A'): [["NoOp"], 'A'],
                     ('A', "Clean", 'B', "Clean", 'B'): [["NoOp"], 'B'],
                     ('A', "Clean", 'B', "Dirty", 'A'): [["Right", "Suck"], 'B'],
                     ('A', "Clean", 'B', "Dirty", 'B'): [["Suck"], 'B'],
                     ('A', "Dirty", 'B', "Clean", 'A'): [["Suck"], 'A'],
                     ('A', "Dirty", 'B', "Clean", 'B'): [["Left", "Suck"], 'A'],
                     ('A', "Dirty", 'B', "Dirty", 'B'): [["Suck", "Left", "Suck"], 'A'],
                     ('A', "Dirty", 'B', "Dirty", 'A'): [["Suck", "Right", "Suck"], 'B'],
                     }
    scoring_pos = 1
    scoring_neg = 1

    def __init__(self, rooms, dirt_config=[]):
        self.configuration = {}
        for x in range(0, len(rooms)):
            self.configuration[rooms[x]] = rooms[x].get_state()

    def get_current_configuration(self):
        return self.configuration

    def current_configuration_readable(self):
        config_copy = {}
        for x in self.configuration:
            config_copy[x.get_name()] = x.get_state()
        return config_copy

    @staticmethod
    def scoring_methodology(agent_obj, percept, room_obj_list, moves):
        percept_score = 0
        if "NoOp" in agent_obj.percept_response_dict[percept][0]:
            agent_obj.scores.append(0)
            return agent_obj.get_score(), percept_score

        if agent_obj.percept_response_dict[percept] == VaccuumEnvironment.__scoring_LUT[percept]:
            print("Correct action. Incrementing a point per action")
            for room in room_obj_list:
                if room.state != "Clean":
                    agent_obj.incOrDecScore(-1, delta=VaccuumEnvironment.scoring_neg)
            percept_score, delta = agent_obj.incOrDecScore(1, delta=VaccuumEnvironment.scoring_pos, moves=moves)
        else:
            print("Wrong action. Decrementing score by a point")
            percept_score, delta = agent_obj.incOrDecScore(-1, delta=VaccuumEnvironment.scoring_neg)
        return agent_obj.get_score(), delta


class VaccuumAgent:
    actions = ["Left", "Right", "Suck", "NoOp"]

    def __init__(self):
        self.score = 0
        self.loc = [0, 0]
        self.room = None
        self.scores = []
        self.percept_response_dict = {}
        self.ind = 0

    def incOrDecScore(self, decider, moves=1, delta=1):
        inc = delta * moves
        if decider == 1:
            self.score += inc
        elif decider == -1:
            self.score -= delta

        self.scores.append(self.score)
        return self.score, inc

    def get_score(self):
        return self.score

    def rule(self, percept):
        action = []
        room_A_obj = 0
        room_A_status = 1
        room_B_status = 3
        room_B_obj = 2
        if percept[room_A_status] == "Dirty" or percept[room_B_status] == "Dirty":  # if 'Dirty'

            if percept[room_A_status] == "Dirty" and percept[room_B_status] == "Dirty":
                if self.room == 'A':
                    action.append("Suck")
                    percept[room_A_obj].set_state("Clean")
                    action.append("Right")
                    self.set_loc(percept[room_B_obj].get_name())
                    action.append("Suck")
                    percept[room_B_obj].set_state("Clean")
                elif self.room == 'B':
                    action.append("Suck")
                    percept[room_B_obj].set_state("Clean")
                    action.append("Left")
                    self.set_loc(percept[room_A_obj].get_name())
                    action.append("Suck")
                    percept[room_A_obj].set_state("Clean")

            elif percept[room_A_status] == "Dirty":
                if self.room == 'A':
                    action.append("Suck")
                    percept[room_A_obj].set_state("Clean")

                elif self.room == 'B':
                    action.append("Left")
                    self.set_loc(percept[room_A_obj].get_name())
                    action.append("Suck")
                    percept[room_A_obj].set_state("Clean")

            elif percept[room_B_status] == "Dirty":
                if self.room == 'B':
                    action.append("Suck")
                    percept[room_B_obj].set_state("Clean")

                elif self.room == 'A':
                    action.append("Right")
                    self.set_loc(percept[room_B_obj].get_name())
                    action.append("Suck")
                    percept[room_B_obj].set_state("Clean")

        else:
            action.append("NoOp")

        return action

    def set_loc(self, loc):
        if loc == 'A':
            self.loc = [0, 0]
            self.room = 'A'
        else:
            self.loc = [0, 1]
            self.room = 'B'


class simple_reflex_vaccuum_agent(VaccuumAgent, VaccuumEnvironment):

    @staticmethod
    def prepare_percept_list(room_obj_list):
        percept_list = []
        for state_1 in Room.room_states:
            for state_2 in Room.room_states:
                for loc in Room.room_names:
                    percept_list.append([room_obj_list[0], state_1, room_obj_list[1], state_2, loc])

        return percept_list

    @staticmethod
    def percept_execute(percept_list, VacAg, Env, room_obj_list):
        for i, percept in enumerate(percept_list):  # [room_obj, state]
            print("\nEvaluating percept ", i+1)

            room_obj_list[0].set_state(percept[1])
            room_obj_list[1].set_state(percept[3])
            VacAg.room = percept[4]

            percept_simplified = (percept[0].get_name(), percept[1], percept[2].get_name(), percept[3], VacAg.room)

            print("(Percept; Robot locn): [{}, {}, {}, {}; {}] ".format(percept[0].get_name(), percept[1],
                                                             percept[2].get_name(), percept[3], VacAg.room))

            action = VacAg.rule(percept)

            print("Action: {}".format(action))

            VacAg.percept_response_dict[percept_simplified] = [action, VacAg.room]
            tot_score, percept_score = Env.scoring_methodology(VacAg, percept_simplified, room_obj_list, len(action))
            print("(#Percept, Configuration State, Robot locn, Percept score, Total Score) : {}, {}, {}, {}, {}".
                  format(i+1, Env.current_configuration_readable(), VacAg.room, percept_score, tot_score))

            print("\n---------------------------------------------------------------------------------------------")

        print("\nPerformance score for each configuration: ", VacAg.scores)
        print("\nAverage score: ", VacAg.score/len(percept_list))

    def start_vacuum(self):

        VacAg = VaccuumAgent()

        loc_rooms = [[0, 0], [0, 1]]
        R_A = Room(loc_rooms[0], 'A')
        R_B = Room(loc_rooms[1], 'B')
        room_obj_list = [R_A, R_B]

        Env = VaccuumEnvironment(room_obj_list)

        percept_list = self.prepare_percept_list(room_obj_list)

        self.percept_execute(percept_list, VacAg, Env, room_obj_list)


"""

Base state : Both room A and room B are clean and robot is situated in room A
Scoring schema: 
    +1 for every right move and both rooms clean
    -1 for every wrong move

"""


if __name__ == "__main__":
    sr_agent = simple_reflex_vaccuum_agent()
    sr_agent.start_vacuum()


