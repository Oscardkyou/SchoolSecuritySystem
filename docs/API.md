# Parent Onboarding Service API Documentation

## Overview
This API provides endpoints for managing parent onboarding in the school security system.

## Base URL
- Development: `http://localhost:5001`
- Production: `https://[EC2_PUBLIC_IP]`

## Endpoints

### Generate Onboarding Link
Creates a unique link for parent photo upload.

- **URL**: `/generate_link`
- **Method**: `POST`
- **Content-Type**: `application/x-www-form-urlencoded`

#### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| parent_name | string | Yes | Parent's first name |
| parent_surname | string | Yes | Parent's last name |
| child_name | string | Yes | Child's full name |

#### Response
```json
{
    "link": "http://[domain]/onboarding/[unique_id]"
}
```

#### Error Response
```json
{
    "error": "Error description"
}
```

### Photo Upload
Handles parent photo upload process.

- **URL**: `/onboarding/<unique_id>`
- **Method**: `GET`, `POST`
- **Content-Type**: `multipart/form-data` (for POST)

#### GET Response
Returns HTML page with photo upload form

#### POST Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| photo | file | Yes | Photo file (JPEG/PNG) |

#### Success Response
```
"Photo uploaded successfully!"
```

#### Error Responses
- `404`: "Invalid link"
- `400`: "No photo uploaded"
- `400`: "No photo selected"

### Admin Dashboard
View all registered parents.

- **URL**: `/`
- **Method**: `GET`
- **Response**: HTML page with parents list

## Error Codes
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Server Error

## AWS CloudWatch Metrics
The following metrics are tracked:
- API Response Times
- Error Rates
- Photo Upload Success Rate
- Invalid Link Attempts

## Security
- All endpoints use HTTPS in production
- File upload size limited to 16MB
- Image validation before storage
- Unique IDs are UUID v4

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
