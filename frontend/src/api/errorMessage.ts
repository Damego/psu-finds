import { ErrorResponseCodes } from "./enums";

export const errorMessages = {
    [ErrorResponseCodes.MISSING_TOKEN]: "Токен аутентификации не обнаружен",
    [ErrorResponseCodes.INVALID_TOKEN]: "Невалидный токен аутентификации",
    [ErrorResponseCodes.INVALID_TOKEN_TYPE]:
      "Некорректный тип токена аутентификации",
    [ErrorResponseCodes.INVALID_USER_CREDENTIALS]:
      "Неверно указана почта или пароль",
    [ErrorResponseCodes.USER_ALREADY_EXISTS]:
      "Пользователь с такой почтой уже существует",
    [ErrorResponseCodes.USER_ALREADY_VERIFIED]:
      "Вы уже подтвердили свою учётную запись",
    [ErrorResponseCodes.USER_NOT_FOUND]: "Пользователь не найден",
    [ErrorResponseCodes.MISSING_PERMISSIONS]: "Это действие доступно только администраторам",
  };
  
  export const getErrorMessage = (code: ErrorResponseCodes) =>
    errorMessages[code] || `Произошла неизвестная ошибка. Код: ${code}`;
  