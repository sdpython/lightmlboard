import os


class TestExAppOptions:

    allowed_users = os.path.join(os.path.dirname(__file__), "users.txt")

    competitions = [dict(name="compet1",
                         data=os.path.join(os.path.dirname(
                             __file__), "off_eval_all_Y.txt"),
                         metric="mean_squared_error")]
