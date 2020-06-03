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

        # Tilt of the drone - membership functions
        self.tilt = ctrl.Antecedent(np.arange(-180, 181, 1), 'tilt')
        self.tilt["negative"] = skfuzzy.trapmf(self.tilt.universe, [-180, -180, -50, -4])
        self.tilt["none"] = skfuzzy.trimf(self.tilt.universe, [-5, 0, 5])
        self.tilt["positive"] = skfuzzy.trapmf(self.tilt.universe, [4, 50, 180, 180])

        # Angular velocity of the drone - membership functions
        self.speed = ctrl.Antecedent(np.arange(-100, 101, 1), 'speed')
        self.speed["negative"] = skfuzzy.trapmf(self.speed.universe, [-100, -100, -30, -5])
        self.speed["none"] = skfuzzy.trimf(self.speed.universe, [-50, 0, 50])
        self.speed["positive"] = skfuzzy.trapmf(self.speed.universe, [5, 30, 100, 100])

        # Power of right engine - membership functions
        self.rightEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'rightEnginePower')
        self.rightEnginePower["low"] = skfuzzy.trapmf(self.rightEnginePower.universe, [0, 0, 25, 25])
        self.rightEnginePower["average"] = skfuzzy.trimf(self.rightEnginePower.universe, [24, 50, 75])
        self.rightEnginePower["high"] = skfuzzy.trimf(self.rightEnginePower.universe, [50, 75, 100])

        # Power of left engine - membership functions
        self.leftEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'leftEnginePower')
        self.leftEnginePower["low"] = skfuzzy.trapmf(self.leftEnginePower.universe, [0, 0, 25, 25])
        self.leftEnginePower["average"] = skfuzzy.trimf(self.leftEnginePower.universe, [24, 50, 75])
        self.leftEnginePower["high"] = skfuzzy.trimf(self.leftEnginePower.universe, [50, 75, 100])

        # Rules defining behaviour of the engines bases on input data (tilt, speed)
        self.ruleT2S2_left = ctrl.Rule(self.tilt['positive'] & self.speed['positive'], self.leftEnginePower['high'])
        self.ruleT2S2_right = ctrl.Rule(self.tilt['positive'] & self.speed['positive'], self.rightEnginePower['low'])

        self.ruleT2S1_left = ctrl.Rule(self.tilt['positive'] & self.speed['none'], self.leftEnginePower['average'])
        self.ruleT2S1_right = ctrl.Rule(self.tilt['positive'] & self.speed['none'], self.rightEnginePower['low'])

        self.ruleT2S0_left = ctrl.Rule(self.tilt['positive'] & self.speed['negative'], self.leftEnginePower['low'])
        self.ruleT2S0_right = ctrl.Rule(self.tilt['positive'] & self.speed['negative'], self.rightEnginePower['low'])

        self.ruleT1S2_left = ctrl.Rule(self.tilt['none'] & self.speed['positive'], self.leftEnginePower['average'])
        self.ruleT1S2_right = ctrl.Rule(self.tilt['none'] & self.speed['positive'], self.rightEnginePower['low'])

        self.ruleT1S1_left = ctrl.Rule(self.tilt['none'] & self.speed['none'], self.leftEnginePower['low'])
        self.ruleT1S1_right = ctrl.Rule(self.tilt['none'] & self.speed['none'], self.rightEnginePower['low'])

        self.ruleT1S0_left = ctrl.Rule(self.tilt['none'] & self.speed['negative'], self.leftEnginePower['low'])
        self.ruleT1S0_right = ctrl.Rule(self.tilt['none'] & self.speed['negative'], self.rightEnginePower['average'])

        self.ruleT0S2_left = ctrl.Rule(self.tilt['negative'] & self.speed['positive'], self.leftEnginePower['low'])
        self.ruleT0S2_right = ctrl.Rule(self.tilt['negative'] & self.speed['positive'], self.rightEnginePower['low'])

        self.ruleT0S1_left = ctrl.Rule(self.tilt['negative'] & self.speed['none'], self.leftEnginePower['low'])
        self.ruleT0S1_right = ctrl.Rule(self.tilt['negative'] & self.speed['none'], self.rightEnginePower['average'])

        self.ruleT0S0_left = ctrl.Rule(self.tilt['negative'] & self.speed['negative'], self.leftEnginePower['low'])
        self.ruleT0S0_right = ctrl.Rule(self.tilt['negative'] & self.speed['negative'], self.rightEnginePower['high'])

        # Controller containing all defined rules
        self.enginePowerCtr = ctrl.ControlSystem([self.ruleT2S2_left, self.ruleT2S2_right,
                                                  self.ruleT2S1_left, self.ruleT2S1_right,
                                                  self.ruleT2S0_left, self.ruleT2S0_right,
                                                  self.ruleT1S2_left, self.ruleT1S2_right,
                                                  self.ruleT1S1_left, self.ruleT1S1_right,
                                                  self.ruleT1S0_left, self.ruleT1S0_right,
                                                  self.ruleT0S2_left, self.ruleT0S2_right,
                                                  self.ruleT0S1_left, self.ruleT0S1_right,
                                                  self.ruleT0S0_left, self.ruleT0S0_right])

    def onCalculateDecision(self) -> AIDecision:
        # angle=0 if drone is not tilted
        angle = (math.degrees(self.droneState.angle - self.droneState.targetAngle) + 180) % 360 - 180
        angularVelocity = self.droneState.angularVelocity * 30

        enginePowering = ctrl.ControlSystemSimulation(self.enginePowerCtr)
        enginePowering.input['tilt'] = angle
        enginePowering.input['speed'] = angularVelocity
        enginePowering.compute()

        left = enginePowering.output['leftEnginePower'] / 1000.0
        right = enginePowering.output['rightEnginePower'] / 1000.0

        return AIDecision(left, right)

