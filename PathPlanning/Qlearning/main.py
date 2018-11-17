# author : 0aqz0
# date: 2018/11/1
import os
import sys
import time
import _thread

from PyQt5.QtCore import QObject, QUrl, pyqtSlot
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QGuiApplication

from RL_brain import QLearningTable


class Maze(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialise the value of the properties.
        self._robot = [1, 1]
        self._start = [1, 1]
        self._end = [9, 9]
        self._obs = []
        self._maxepisode = 100
        self._learningrate = 0.01
        self._discountfactor = 0.9
        self._egreedy = 0.9
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.newpathplanning = False
        self.finalpath = []
        self.isfinalpath = False
        self.currentepisode = 0
        self.currentqtable = ""

    @pyqtSlot(int, int)
    def setstart(self, x, y):
        global root
        self._start[0] = x
        self._start[1] = y
        self._robot = self._start
        # print(self._start)

    @pyqtSlot(int, int)
    def setend(self, x, y):
        global root
        self._end[0] = x
        self._end[1] = y
        # print(self._end)

    @pyqtSlot(int, int)
    def setobs(self, x, y):
        global root
        if [x,y] not in self._obs:
            self._obs.append([x,y])
        # print(self._obs)

    @pyqtSlot()
    def reset(self):
        global root
        self._robot = [1, 1]
        self._start = [1, 1]
        self._end = [9, 9]
        self._obs = []
        self.finalpath = []
        self.isfinalpath = False
        self.currentepisode = 0
        self.currentqtable = ""
        root.resetqml()

    @pyqtSlot(bool)
    def setnewpathplanning(self, setter):
        self.newpathplanning = setter
        # print(self.newpathplanning)

    @pyqtSlot(result = str)
    def robotstring(self):
        return str("(" + str(int(self._robot[0])) + "," + str(int(self._robot[1])) + ")")

    @pyqtSlot(result = str)
    def endstring(self):
        return str("(" + str(int(self._end[0])) + "," + str(int(self._end[1])) + ")")

    @pyqtSlot(result = 'QStringList')
    def obsstring(self):
        return [str("(" + str(int(obs[0])) + "," + str(int(obs[1])) + ")") for obs in self._obs]

    @pyqtSlot(result = int)
    def obsnum(self):
        return len(self._obs)

    @pyqtSlot()
    def quit(self):
        sys.exit(0)

    @pyqtSlot(int)
    def maxepisode(self, maxepisode):
        self._maxepisode = maxepisode
        # print(self._maxepisode)

    @pyqtSlot(float)
    def learningrate(self, learningrate):
        self._learningrate = learningrate
        # print(self._learningrate)

    @pyqtSlot(float)
    def discountfactor(self, discountfactor):
        self._discountfactor = discountfactor
        # print(self._discountfactor)

    @pyqtSlot(float)
    def egreedy(self, egreedy):
        self._egreedy = egreedy
        # print(self._egreedy)

    # @pyqtSlot()
    # def printinfo(self):
    #     print("updated")

    @pyqtSlot(result = 'QStringList')
    def finalpathlist(self):
        return self.finalpath

    @pyqtSlot(result = int)
    def finalpathlen(self):
        return len(self.finalpath)

    @pyqtSlot(result = bool)
    def requestisfinalpath(self):
        return self.isfinalpath

    @pyqtSlot(result = int)
    def requestepisode(self):
        return self.currentepisode

    @pyqtSlot(result = "QString")
    def requestqtable(self):
        return self.currentqtable

    @pyqtSlot()
    def go(self):
        self.newpathplanning = True

    # observation after action
    @pyqtSlot()
    def step(self, action):
        global root
        # next state
        next_s = self._robot
        if action == 0:
            if next_s[1] > 1:
                next_s[1] -= 1
        elif action == 1:
            if next_s[1] < 9:
                next_s[1] += 1
        elif action == 2:
            if next_s[0] > 1:
                next_s[0] -= 1
        elif action == 3:
            if next_s[0] < 9:
                next_s[0] += 1

        # move to next state
        self._robot = next_s

        # reward
        if next_s == self._end:
            reward = 10
            done = True
            next_s = 'terminal'
            # print("win")
            return next_s, reward, done
        # punish
        for obs in self._obs:
            if next_s == obs:
                reward = -10
                done = True
                next_s = 'terminal'
                # print("fail")
                return next_s, reward, done
        # nothing
        reward = -1
        done = False
        return str(next_s), reward, done

    @pyqtSlot()
    def pathplanning(self):
        global root
        global view
        RL = QLearningTable(actions=list(range(self.n_actions)), learning_rate=self._learningrate,
                            reward_decay=self._discountfactor, e_greedy=self._egreedy)
        # update qtable
        self.currentqtable = str(RL.q_table)
        for episode in range(self._maxepisode):
            # update episode
            self.currentepisode = episode + 1

            # reset
            self._robot = self._start.copy()
            # initialize observation
            observation = str(self._robot)
            time.sleep(1)

            while True:
                # record the final path
                if(episode == self._maxepisode - 1):
                    self.finalpath.append(str("(" + str(int(self._robot[0])) + "," + str(int(self._robot[1])) + ")"))

                # choose action
                action = RL.choose_action(observation)
                # get new observation
                next_observation, reward, done = self.step(action)
                # learn from this observation
                RL.learn(observation,action,reward,next_observation)
                # update observation
                observation = next_observation

                # update qtable
                self.currentqtable = str(RL.q_table)
                # sleep for qml's update
                time.sleep(0.2)
                # print("#######")
                if done:
                    break
            # print(self.finalpath)
        self.isfinalpath = True


if __name__ == '__main__':
    # create maze instance
    maze = Maze()
    # start a new thread
    def threadforpathplanning():
        while True:
            if maze.newpathplanning:
                maze.pathplanning()
                maze.newpathplanning = False
            time.sleep(0.5)
    _thread.start_new_thread(threadforpathplanning,())

    # create application instance
    app = QGuiApplication(sys.argv)
    view = QQuickView()

    # register the python type
    # qmlRegisterType(Maze, 'Maze', 1, 0, 'Maze')

    qmlFile = os.path.join(os.path.dirname(__file__), 'view.qml')

    context = view.rootContext()
    context.setContextProperty("maze", maze)

    view.setSource(QUrl.fromLocalFile(os.path.abspath(qmlFile)))
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    root = view.rootObject()

    res = app.exec_()

    # delete the view
    del view
    sys.exit(res)
