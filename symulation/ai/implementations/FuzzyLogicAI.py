import math

from DebugScreen import DebugScreen
from ai.AIComponent import AIComponent
from ai.AIDecision import AIDecision
import numpy as np
import skfuzzy
from skfuzzy import control as ctrl


class FuzzyLogicAI(AIComponent):

    def __init__(self):
        super().__init__()
        #
        # self.tilt = ctrl.Antecedent(np.arange(-180, 181, 1), 'tilt')
        # self.tilt['negative'] = skfuzzy.trimf(self.tilt.universe, [-90, -45, 0])
        # self.tilt['veryNegative'] = skfuzzy.trapmf(self.tilt.universe, [-180, -180, -90, -45])
        # self.tilt['neutral'] = skfuzzy.trimf(self.tilt.universe, [-45, 0, 45])
        # self.tilt['positive'] = skfuzzy.trimf(self.tilt.universe, [0, 45, 90])
        # self.tilt['veryPositive'] = skfuzzy.trapmf(self.tilt.universe, [45, 90, 180, 180])
        # # self.tilt.view()
        #
        # self.rightEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'rightEnginePower')
        # self.rightEnginePower["pass"] = skfuzzy.trimf(self.rightEnginePower.universe, [0, 0, 1])
        # self.rightEnginePower["low"] = skfuzzy.trimf(self.rightEnginePower.universe, [0, 5, 20])
        # self.rightEnginePower["high"] = skfuzzy.trapmf(self.rightEnginePower.universe, [5, 20, 100, 100])
        #
        # # self.rightEnginePower.view()
        #
        # self.leftEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'leftEnginePower')
        #
        # self.leftEnginePower["pass"] = skfuzzy.trimf(self.leftEnginePower.universe, [0, 0, 1])
        # self.leftEnginePower["low"] = skfuzzy.trimf(self.leftEnginePower.universe, [0, 5, 20])
        # self.leftEnginePower["high"] = skfuzzy.trapmf(self.leftEnginePower.universe, [5, 20, 100, 100])
        #
        # # self.leftEnginePower.view()
        #
        # self.ruleRight1 = ctrl.Rule(self.tilt['positive'], self.leftEnginePower['low'])
        # self.ruleRight2 = ctrl.Rule(self.tilt['veryPositive'], self.leftEnginePower['high'])
        # self.ruleLeft1 = ctrl.Rule(self.tilt['negative'], self.rightEnginePower['low'])
        # self.ruleLeft2 = ctrl.Rule(self.tilt['veryNegative'], self.rightEnginePower['high'])
        # self.ruleRight0 = ctrl.Rule(self.tilt['neutral'], self.leftEnginePower['pass'])
        # self.ruleLeft0 = ctrl.Rule(self.tilt['neutral'], self.rightEnginePower['pass'])
        #
        # self.enginePowerCtr = ctrl.ControlSystem([self.ruleRight1, self.ruleRight2, self.ruleLeft1,
        #                                           self.ruleLeft2, self.ruleRight0, self.ruleLeft0])

        self.tilt = ctrl.Antecedent(np.arange(-180, 181, 1), 'tilt')
        self.tilt.automf(5)

        self.rightEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'rightEnginePower')
        self.rightEnginePower.automf(5)
        self.leftEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'leftEnginePower')
        self.leftEnginePower.automf(5)

        self.ruleRight2 = ctrl.Rule(self.tilt['good'], self.leftEnginePower['good'])
        self.ruleRight22 = ctrl.Rule(self.tilt['good'], self.rightEnginePower['poor'])

        self.ruleRight1 = ctrl.Rule(self.tilt['decent'], self.leftEnginePower['average'])
        self.ruleRight11 = ctrl.Rule(self.tilt['decent'], self.rightEnginePower['poor'])

        self.ruleRight0 = ctrl.Rule(self.tilt['average'], self.leftEnginePower['poor'])
        self.ruleLeft0 = ctrl.Rule(self.tilt['average'], self.rightEnginePower['poor'])

        self.ruleLeft1 = ctrl.Rule(self.tilt['mediocre'], self.leftEnginePower['poor'])
        self.ruleLeft11 = ctrl.Rule(self.tilt['mediocre'], self.rightEnginePower['average'])

        self.ruleLeft2 = ctrl.Rule(self.tilt['poor'], self.leftEnginePower['poor'])
        self.ruleLeft22 = ctrl.Rule(self.tilt['poor'], self.rightEnginePower['good'])


        self.tilt.view()
        self.rightEnginePower.view()
        self.leftEnginePower.view()

        self.enginePowerCtr = ctrl.ControlSystem([self.ruleRight1,self.ruleRight11, self.ruleRight2, self.ruleRight22,
                                                  self.ruleLeft1, self.ruleLeft11, self.ruleLeft2, self.ruleLeft22,
                                                  self.ruleRight0, self.ruleLeft0])

    def onCalculateDecision(self) -> AIDecision:
        angle = (math.degrees(self.droneState.angle) + 180) % 360 - 180
        print(angle)
        # DebugScreen.getInstance().addInfo("target angle", self.droneState.targetAngle)
        # DebugScreen.getInstance().addInfo("angle", "{:.4f}".format(self.droneState.angle))
        # DebugScreen.getInstance().addInfo("angle vel", self.droneState.angularVelocity)

        enginePowering = ctrl.ControlSystemSimulation(self.enginePowerCtr)
        enginePowering.input['tilt'] = angle
        enginePowering.compute()
        right = enginePowering.output['rightEnginePower'] / 1000.0
        left = enginePowering.output['leftEnginePower'] / 1000.0
        print('left=', left)
        print('right=', right)
        return AIDecision(left, right)

