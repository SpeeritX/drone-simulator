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

        self.tilt = ctrl.Antecedent(np.arange(-180, 181, 1), 'tilt')
        self.tilt["poor"] = skfuzzy.trapmf(self.tilt.universe, [-180, -180, -50, -4])
        self.tilt["average"] = skfuzzy.trimf(self.tilt.universe, [-5, 0, 5])
        self.tilt["good"] = skfuzzy.trapmf(self.tilt.universe, [4, 50, 180, 180])

        self.speed = ctrl.Antecedent(np.arange(-100, 101, 1), 'speed')
        self.speed["poor"] = skfuzzy.trapmf(self.speed.universe, [-100, -100, -30, -5])
        self.speed["average"] = skfuzzy.trimf(self.speed.universe, [-50, 0, 50])
        self.speed["good"] = skfuzzy.trapmf(self.speed.universe, [5, 30, 100, 100])

        self.rightEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'rightEnginePower')
        self.rightEnginePower["poor"] = skfuzzy.trapmf(self.rightEnginePower.universe, [0, 0, 25, 25])
        self.rightEnginePower["average"] = skfuzzy.trimf(self.rightEnginePower.universe, [24, 50, 75])
        self.rightEnginePower["good"] = skfuzzy.trimf(self.rightEnginePower.universe, [50, 75, 100])

        self.leftEnginePower = ctrl.Consequent(np.arange(0, 101, 1), 'leftEnginePower')
        self.leftEnginePower["poor"] = skfuzzy.trapmf(self.leftEnginePower.universe, [0, 0, 25, 25])
        self.leftEnginePower["average"] = skfuzzy.trimf(self.leftEnginePower.universe, [24, 50, 75])
        self.leftEnginePower["good"] = skfuzzy.trimf(self.leftEnginePower.universe, [50, 75, 100])

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

        self.enginePowerCtr = ctrl.ControlSystem([self.ruleT2S2_1, self.ruleT2S2_2, self.ruleT2S1_1, self.ruleT2S1_2,
                                                  self.ruleT2S0_1, self.ruleT2S0_2,
                                                  self.ruleT1S2_1, self.ruleT1S2_2, self.ruleT1S1_1, self.ruleT1S1_2,
                                                  self.ruleT1S0_1, self.ruleT1S0_2,
                                                  self.ruleT0S2_1, self.ruleT0S2_2, self.ruleT0S1_1, self.ruleT0S1_2,
                                                  self.ruleT0S0_1, self.ruleT0S0_2])


    def onCalculateDecision(self) -> AIDecision:
        angle = (math.degrees(self.droneState.angle - self.droneState.targetAngle) + 180) % 360 - 180
        angularVelocity = self.droneState.angularVelocity * 30

        enginePowering = ctrl.ControlSystemSimulation(self.enginePowerCtr)
        enginePowering.input['tilt'] = angle
        enginePowering.input['speed'] = angularVelocity
        enginePowering.compute()

        left = enginePowering.output['leftEnginePower'] / 1000.0
        right = enginePowering.output['rightEnginePower'] / 1000.0

        return AIDecision(left, right)

