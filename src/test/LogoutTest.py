from test.helpers.PDUnitTest import PDUnitTest, test
from test.helpers.UserUtil import UserUtil

class LogoutTest(PDUnitTest, UserUtil):

    def setUp(self):
        PDUnitTest.setUp(self)
        form = self.prepareLoginForm()
        self.controller.doLogin(form)

    @test
    def you_can_log_out(self):
        resp = self.controller.doLogout()
        self.assertEquals(resp.status_code, 200)
        self.assertEqual('{"message": "logged out"}', self.getResponseText(resp))

    @test
    def if_you_log_out_you_will_be_logged_out(self):
        self.assertTrue(self.controller.getCurrentUser().is_authenticated())
        self.controller.doLogout()
        self.assertFalse(self.controller.getCurrentUser().is_authenticated())
