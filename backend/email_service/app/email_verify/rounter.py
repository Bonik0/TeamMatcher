from fastapi import APIRouter, Depends
from app.email_verify.schemas import (
    SendEmailIn,
    VerifyCodeOut,
    VerifyCodeIn,
    SendEmailOut,
)
from app.email_verify.utils import EmailVerifyUtils
from app.email_verify.dependencies.use_cases import (
    get_save_code_use_case,
    get_verify_code_use_case,
    get_success_verify_use_case,
)
from app.email_verify.use_cases.save_code import SaveVerificationCodeUseCase
from app.email_verify.use_cases.verify_code import VerifyCodeUseCase
from app.email_verify.dependencies.utils import get_email_verify_utils
from app.email_verify.use_cases.success_verify import SuccessVerifyUseCase


router = APIRouter(prefix="/code", tags=["Checking the mail code"])


@router.post(path="/send", summary="Sending code")
async def send_email(
    form: SendEmailIn,
    save_use_case: SaveVerificationCodeUseCase = Depends(get_save_code_use_case),
    utils: EmailVerifyUtils = Depends(get_email_verify_utils),
) -> SendEmailOut:
    code, op_id = utils.generate_code(), utils.generate_operation_id()
    await save_use_case.execute(form.email, code, op_id)
    return SendEmailOut(operation_id=op_id)


@router.post(path="/verify", summary="Verify code")
async def verify_code(
    form: VerifyCodeIn,
    verify_code_use_case: VerifyCodeUseCase = Depends(get_verify_code_use_case),
    success_verify_use_case: SuccessVerifyUseCase = Depends(
        get_success_verify_use_case
    ),
) -> VerifyCodeOut:
    is_correct_code, verification_code = await verify_code_use_case.execute(
        form.email, form.code, form.operation_id
    )

    if is_correct_code:
        await success_verify_use_case.execute(verification_code)

    return VerifyCodeOut(is_correct_code=is_correct_code)
