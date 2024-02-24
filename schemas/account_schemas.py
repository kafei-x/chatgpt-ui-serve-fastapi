from pydantic import BaseModel, Field
from models.account_model import User

class AccountAdd(BaseModel):
    username: str = Field()
    email: str = Field()
    password1: str = Field()
    password2: str = Field()
    code: str = Field()

    def validate_passwords(self):
        errmsg = []
        if self.password1 != self.password2:
            return errmsg.append({"password":["password1 and password2 don't match"]})
        return errmsg  
    
    async def validate_account_not_exist(self):
        errmsg = []
        if await User.get_or_none(username=self.username):
            errmsg.append({"username":["A user with that username already exists."]})
        if await User.get_or_none(email=self.email):
            errmsg.append({"email":["A user is already registered with this e-mail address."]})
        
        return errmsg


class AccountLogin(BaseModel):
    username: str = Field()
    password: str = Field()
