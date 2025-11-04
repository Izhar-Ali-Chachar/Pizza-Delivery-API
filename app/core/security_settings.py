from fastapi.security import OAuth2PasswordBearer

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")
oauth2_scheme_driver = OAuth2PasswordBearer(tokenUrl="/delivery/sign-in")