from .conftest import *


# @patch("src.com.sql.UserSqlTable")
# @patch("src.website.action.dashboard.getUsername")
# # @pytest.mark.parametrize(("df", "expected"), UnittestFiles.pipeline_test_values)
# def test_dashboard_mixin_colors(fake_user_table, fake_get_username):
#     fake_get_username.return_value = "hello"

#     dashboard_page = DashboardHomePage(MagicMock())
#     selected_date = "2019-09-01"
#     period = "month"
#     response = dashboard_page.updateGraph(selected_date, period, None)
#     breakpoint()
