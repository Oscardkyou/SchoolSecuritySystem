# API Documentation

## Summary
API для системы безопасности школы, обеспечивающее функционал генерации ссылок и загрузки фотографий родителей.

## What
REST API предоставляет следующие возможности:
- Генерация уникальных ссылок для родителей
- Загрузка и сохранение фотографий
- Получение информации о родителях

## Why
API разработано для обеспечения:
- Безопасного процесса онбординга родителей
- Удобного способа загрузки фотографий
- Надежного хранения данных

## How

### Endpoints

#### 1. Генерация ссылки для родителя

```http
POST /generate_link
Content-Type: application/x-www-form-urlencoded
```

**Parameters**
| Имя | Тип | Обязательно | Описание |
|-----|-----|-------------|-----------|
| parent_name | string | Да | Имя родителя |
| parent_surname | string | Да | Фамилия родителя |
| child_name | string | Да | Имя ребенка |

**Response**
```json
{
    "link": "http://localhost:5001/onboarding/123e4567-e89b-12d3-a456-426614174000"
}
```

#### 2. Страница онбординга

```http
GET /onboarding/<unique_id>
```

**Parameters**
| Имя | Тип | Обязательно | Описание |
|-----|-----|-------------|-----------|
| unique_id | string | Да | Уникальный идентификатор родителя |

**Response**
- HTML страница с формой загрузки фото

#### 3. Загрузка фото

```http
POST /onboarding/<unique_id>
Content-Type: multipart/form-data
```

**Parameters**
| Имя | Тип | Обязательно | Описание |
|-----|-----|-------------|-----------|
| unique_id | string | Да | Уникальный идентификатор родителя |
| photo | file | Да | Файл фотографии (JPG/PNG) |

**Response**
- 200: "Photo uploaded successfully!"
- 400: "No photo uploaded" или "No photo selected"
- 404: "Invalid link"

## Troubleshooting

### Общие ошибки

1. **404 Not Found**
   - Проверьте правильность unique_id
   - Убедитесь, что ссылка не устарела

2. **400 Bad Request**
   - Проверьте наличие всех обязательных полей
   - Убедитесь, что фото прикреплено

3. **500 Internal Server Error**
   - Проверьте подключение к базе данных
   - Проверьте права на директорию uploads

## Examples

### Пример создания ссылки

```bash
curl -X POST http://localhost:5001/generate_link \
  -d "parent_name=Иван" \
  -d "parent_surname=Петров" \
  -d "child_name=Мария"
```

### Пример загрузки фото

```bash
curl -X POST http://localhost:5001/onboarding/123e4567-e89b-12d3-a456-426614174000 \
  -F "photo=@photo.jpg"
```

## References
- [Flask File Uploads](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Multipart Form Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type)
