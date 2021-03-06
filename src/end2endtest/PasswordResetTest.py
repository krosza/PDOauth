from twatson.unittest_annotations import Fixture, test
from end2endtest.helpers.BrowsingUtil import BrowsingUtil, TE


class PasswordResetTest(Fixture,BrowsingUtil):

    @test
    def password_can_be_reset_using_the_reset_link(self):
        password = "Ez3gyJelsz0"
        user = self.getAssurerUser()
        self.doPasswordResetWithNewPassword(password)
        oldPassword=user.password
        user.password=password
        self.loginWithPasswordAs(user)
        self.assertTextInMeMsg(user.email)  # @UndefinedVariable
        self.logOut()
        TE.assurerUser.password=oldPassword
        self.doPasswordResetWithNewPassword(oldPassword)
