"""
This file serves to define "CONSTANTS" to replace all occurrences of
"magic strings" within the backend packages.

It also contains some default values for the simulation (e.g. RTOL, ATOL).
"""

__author__ = 'Moritz Wade'

# defining options (enum-like)
OPTIONS_IDENTIFICATION_BACKEND = ["nlscon", "parkin"]
# 10.02.15 td: added options (enums) for possible numerical integrator
OPTIONS_INTEGRATOR_BACKEND = ["limex", "metan1", "dop853"]

OPTION_PARAMETER_CONSTRAINT_NONE = "No Constraints"
OPTION_PARAMETER_CONSTRAINT_POSITIVITY = "Positivity (Exponential Transformation)"
OPTION_PARAMETER_CONSTRAINT_LOWERBOUND = "Lower Bound"
OPTION_PARAMETER_CONSTRAINT_UPPERBOUND = "Upper Bound"
OPTION_PARAMETER_CONSTRAINT_INTERVAL = "Interval (Lower and Upper)"

OPTIONS_PARAMETER_CONSTRAINT_TYPES = [OPTION_PARAMETER_CONSTRAINT_NONE,
                                      OPTION_PARAMETER_CONSTRAINT_POSITIVITY,
                                      OPTION_PARAMETER_CONSTRAINT_LOWERBOUND,
                                      OPTION_PARAMETER_CONSTRAINT_UPPERBOUND,
                                      OPTION_PARAMETER_CONSTRAINT_INTERVAL]

# DEFAULT VALUES

# 04.03.13 td: added default value for cubic Hermite interpolation (disabled)
DEFAULT_CUBIC_HERMITE = False

DEFAULT_STARTTIME = 0
DEFAULT_ENDTIME = 100
DEFAULT_NUMBER_INTERVALS = 100

DEFAULT_RTOL = "1E-07"
DEFAULT_ATOL = "1E-09"
DEFAULT_XTOL = "1E-03"
#DEFAULT_RTOL = "1E-06" 
#DEFAULT_ATOL = "1E-12" 
#DEFAULT_XTOL = "1E-04" 
DEFAULT_MAX_NUM_NEWTON_STEPS = 50
DEFAULT_SD_SPECIES = "1.0"

DEFAULT_NO_AUTO_ROW_SCALING = False
DEFAULT_JACOBIAN = 1 # 3
DEFAULT_PROBLEM_TYPE = 3
DEFAULT_RESIDUAL_SCALING = 1
DEFAULT_PARAMETER_CONSTRAINTS = OPTIONS_PARAMETER_CONSTRAINT_TYPES[0]
DEFAULT_PARAMETER_CONSTRAINTS_LOWERBOUND = -1.0 # float("-inf")
DEFAULT_PARAMETER_CONSTRAINTS_UPPERBOUND = 1.0 # float("inf")
DEFAULT_PARAMETER_CONSTRAINTS_PER_PARAMETER = False


DEFAULT_USE_MEASURED_TIMEPOINTS = False
DEFAULT_IDENTIFICATION_BACKEND = OPTIONS_IDENTIFICATION_BACKEND[0]
# 10.02.15 td: added default value for numerical integrator (LIMEX)
DEFAULT_INTEGRATOR_BACKEND = OPTIONS_INTEGRATOR_BACKEND[0]


#### CONSTANT STRINGS ###
# (for accessing dictionaries, etc.)

# 04.03.13 td: added option setting for cubic Hermite interpolation
SETTING_USE_CUBIC_HERMITE = "setting_use_cubic_hermite"

SETTING_STARTTIME = "setting_starttime"
SETTING_ENDTIME = "setting_endtime"
SETTING_NUMBER_TIMEPOINTS = "setting_number_timepoints"
SETTING_RTOL = "setting_tolerance1"
SETTING_ATOL = "setting_tolerance2"
SETTING_XTOL = "setting_xtol"
SETTING_SD_SPECIES = "setting_tolerance3"
SETTING_MAX_NUM_NEWTON_STEPS = "setting_max_num_newton_steps"
SETTING_USE_MEASURED_TIMEPOINTS = "setting_use_measured_timepoints"

SETTING_IDENTIFICATION_BACKEND = "setting_identification_backend"
# 10.02.15 td: added option setting for numerical integrator backend
SETTING_INTEGRATOR_BACKEND = "setting_integrator_backend"


SETTING_NO_AUTO_ROW_SCALING = "setting_no_auto_row_scaling"
SETTING_JACOBIAN = "setting_jacobian"
SETTING_PROBLEM_TYPE = "setting_problem_type"
SETTING_RESIDUAL_SCALING = "setting_residual_scaling"
SETTING_PARAMETER_CONSTRAINTS = "setting_parameter_constraints"
SETTING_PARAMETER_CONSTRAINTS_LOWERBOUND = "setting_parameter_constraints_lowerbound"
SETTING_PARAMETER_CONSTRAINTS_UPPERBOUND = "setting_parameter_constraints_upperbound"
SETTING_PARAMETER_CONSTRAINTS_PER_PARAMETER = "setting_parameter_constraints_per_parameter"

MODE_INTEGRATE = "mode_integrate"
MODE_SENSITIVITIES_OVERVIEW = "mode_sensitivities_overview"
MODE_SENSITIVITIES_DETAILS = "mode_sensitivities_details"
MODE_PARAMETER_ESTIMATION = "mode_parameter_estimation"

FINISHED_INTEGRATION = "Integration finished"
FINISHED_SENSITIVITY_OVERVIEW = "Computation of Sensitivity Overview finished"
FINISHED_SENSITIVITY_DETAILS = "Computation of Sensitivity Details finished"
FINISHED_PARAMETER_ESTIMATION = "Completed Parameter Identification"

SIMULATION_RESULTS = "Simulation Results"

SENSITIVITY_TRAJECTORIES = "Sensitivity Overview"
SENSITIVITY_RAW_JACOBIAN = "Sensitivities (Jacobian)"
SENSITIVITY_PER_PARAM_AND_SPECIES = "Sensitivities"
SENSITIVITY_PER_PARAM = "Sensitivities (per Parameter)"
SENSITIVITY_SUBCONDITION_PER_PARAM = "Subconditions"

SUBCONDITION_HEADER_ABSOLUTE = "Subcondition (abs.)"
