import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# 1) Tizim loglari
system_logger = logging.getLogger("system_logger")
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler(os.path.join(LOGS_DIR, "system.log"), encoding="utf-8")
system_handler.setFormatter(logging.Formatter("%(asctime)s - [SYSTEM] - %(levelname)s - %(message)s"))
system_logger.addHandler(system_handler)


# 2) Foydalanuvchi amallari loglari
action_logger = logging.getLogger("action_logger")
action_logger.setLevel(logging.INFO)
action_handler = logging.FileHandler(os.path.join(LOGS_DIR, "actions.log"), encoding="utf-8")
action_handler.setFormatter(logging.Formatter("%(asctime)s - USER_ID:%(user_id)s - NAME:%(full_name)s - ACTION:%(message)s"))
action_logger.addHandler(action_handler)





def log_action(user, action: str):
    extra = {"user_id": user.id, "full_name": user.full_name}
    action_logger.info(action, extra=extra)


def log_system(message: str, level="info"):
    if level == "error":
        system_logger.error(message)
    elif level == "warning":
        system_logger.warning(message)
    else:
        system_logger.info(message)
