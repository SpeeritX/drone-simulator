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
        self.tilt["poor"] = skfuzzy.trapmf(self.tilt.universe, [-180, -180, -20, 0])
        self.tilt["average"] = skfuzzy.trimf(self.tilt.universe, [-5, 0, 5])
        self.tilt["good"] = skfuzzy.trapmf(self.tilt.universe, [0, 20, 180, 180])

        self.speed = ctrl.Antecedent(np.arange(-100, 101, 1), 'speed')

        self.speed["poor"] = skfuzzy.trapmf(self.speed.universe, [-100, -100, -30, 10])
        self.speed["average"] = skfuzzy.trimf(self.speed.universe, [-50, 0, 50])
        self.speed["good"] = skfuzzy.trapmf(self.speed.universe, [-10, 30, 100, 100])
        self.speed.view()

        self.rightEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'rightEnginePower')
        self.rightEnginePower.automf(3)
        self.leftEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'leftEnginePower')
        self.leftEnginePower.automf(3)

        self.ruleT2S2_1 = ctrl.Rule(self.tilt['good'] & self.speed['good'], self.leftEnginePower['good'])
        self.ruleT2S2_2 = ctrl.Rule(self.tilt['good'] & self.speed['good'], self.rightEnginePower['poor'])

        self.ruleT2S1_1 = ctrl.Rule(self.tilt['good'] & self.speed['average'], self.leftEnginePower['average'])
        self.ruleT2S1_2 = ctrl.Rule(self.tilt['good'] & self.speed['average'], self.rightEnginePower['poor'])

        self.ruleT2S0_1 = ctrl.Rule(self.tilt['good'] & self.speed['poor'], self.leftEnginePower['poor'])
        self.ruleT2S0_2 = ctrl.Rule(self.tilt['good'] & self.speed['poor'], self.rightEnginePower['poor'])


        self.ruleT1S2_1 = ctrl.Rule(self.tilt['average'] & self.speed['good'], self.leftEnginePower['average'])
        self.ruleT1S2_2 = ctrl.Rule(self.tilt['average'] & self.speed['good'], self.rightEnginePower['poor'])

        self.ruleT1S1_1 = ctrl.Rule(self.tilt['average'] & self.speed['average'], self.leftEnginePower['poor'])
        self.ruleT1S1_2 = ctrl.Rule(self.tilt['average'] & self.speed['average'], self.rightEnginePower['poor'])

        self.ruleT1S0_1 = ctrl.Rule(self.tilt['average'] & self.speed['poor'], self.leftEnginePower['poor'])
        self.ruleT1S0_2 = ctrl.Rule(self.tilt['average'] & self.speed['poor'], self.rightEnginePower['average'])


        self.ruleT0S2_1 = ctrl.Rule(self.tilt['poor'] & self.speed['good'], self.leftEnginePower['poor'])
        self.ruleT0S2_2 = ctrl.Rule(self.tilt['poor'] & self.speed['good'], self.rightEnginePower['poor'])

        self.ruleT0S1_1 = ctrl.Rule(self.tilt['poor'] & self.speed['average'], self.leftEnginePower['poor'])
        self.ruleT0S1_2 = ctrl.Rule(self.tilt['poor'] & self.speed['average'], self.rightEnginePower['average'])

        self.ruleT0S0_1 = ctrl.Rule(self.tilt['poor'] & self.speed['poor'], self.leftEnginePower['poor'])
        self.ruleT0S0_2 = ctrl.Rule(self.tilt['poor'] & self.speed['poor'], self.rightEnginePower['good'])


        self.tilt.view()
        self.rightEnginePower.view()
        self.leftEnginePower.view()

        self.enginePowerCtr = ctrl.ControlSystem([self.ruleT2S2_1, self.ruleT2S2_2, self.ruleT2S1_1, self.ruleT2S1_2,
                                                  self.ruleT2S0_1, self.ruleT2S0_2,
                                                  self.ruleT1S2_1, self.ruleT1S2_2, self.ruleT1S1_1, self.ruleT1S1_2,
                                                  self.ruleT1S0_1, self.ruleT1S0_2,
                                                 self.ruleT0S2_1, self.ruleT0S2_2, self.ruleT0S1_1, self.ruleT0S1_2,
                                                  self.ruleT0S0_1, self.ruleT0S0_2])

    def onCalculateDecision(self) -> AIDecision:
        angle = (math.degrees(self.droneState.angle - self.droneState.targetAngle) + 180) % 360 - 180
        # angle = (math.degrees(self.droneState.angle) + 180) % 360 - 180
        print(angle)
        angularVelocity = self.droneState.angularVelocity * 30
        print(angularVelocity)
        # DebugScreen.getInstance().addInfo("target angle", self.droneState.targetAngle)
        # DebugScreen.getInstance().addInfo("angle", "{:.4f}".format(self.droneState.angle))
        # DebugScreen.getInstance().addInfo("angle vel", self.droneState.angularVelocity)

        enginePowering = ctrl.ControlSystemSimulation(self.enginePowerCtr)
        enginePowering.input['tilt'] = angle
        enginePowering.input['speed'] = angularVelocity
        enginePowering.compute()
        right = enginePowering.output['rightEnginePower'] / 1000.0
        left = enginePowering.output['leftEnginePower'] / 1000.0
        print('left=', left)
        print('right=', right)
        return AIDecision(left, right)

