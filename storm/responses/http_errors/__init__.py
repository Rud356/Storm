from functools import partial

from .http_exception import HttpError

# Errors with codes 4XX
BadRequest = partial(HttpError, status=400, message="Bad request")
Unauthorized = partial(HttpError, status=401, message="Unauthorized")
PaymentRequired = partial(HttpError, status=402, message="Payment required")
Forbidden = partial(HttpError, status=403, message="Forbidden")
NotFound = partial(HttpError, status=404, message="Not found")
MethodNotAllowed = partial(HttpError, status=405, message="Method not allowed")
NotAcceptable = partial(HttpError, status=406, message="Not acceptable")
ProxyAuthenticationRequired = partial(
    HttpError, status=407, message="Proxy Authentication Required"
)
RequestTimeout = partial(HttpError, status=408, message="Request timeout")
Conflict = partial(HttpError, status=409, message="Conflict")
Gone = partial(HttpError, status=410, message="Gone")
LengthRequired = partial(HttpError, status=411, message="Length required")
PreconditionFailed = partial(
    HttpError, status=412, message="Precondition failed"
)
PayloadTooLarge = partial(HttpError, status=413, message="Payload too large")
URITooLong = partial(HttpError, status=414, message="Uri too long")
UnsupportedMediaType = partial(
    HttpError, status=415, message="Unsupported media type"
)
RangeNotSatisfiable = partial(
    HttpError, status=416, message="Range not satisfiable"
)
ExpectationFailed = partial(
    HttpError, status=417, message="Expectation failed"
)
IAmATeapot = partial(HttpError, status=418, message="I am a teapot")
AuthenticationTimeout = partial(
    HttpError, status=419, message="Authentication failed"
)
MisdirectedRequest = partial(
    HttpError, status=421, message="Misdirected request"
)
UnprocessableEntity = partial(
    HttpError, status=422, message="Unprocessable entity"
)
Locked = partial(HttpError, status=423, message="Locked")
FailedDependency = partial(HttpError, status=424, message="Failed dependency")
TooEarly = partial(HttpError, status=425, message="Too early")
UpgradeRequired = partial(HttpError, status=426, message="Upgrade required")
PreconditionRequired = partial(
    HttpError, status=428, message="Precondition required"
)
TooManyRequests = partial(HttpError, status=429, message="Too many requests")
RequestHeaderFieldsTooLarge = partial(
    HttpError, status=431, message="Request header fields too large"
)
RetryWith = partial(HttpError, status=449, message="Retry with")
UnavailableForLegalReasons = partial(
    HttpError, status=451, message="Unavailable for legal reasons"
)
ClientClosedRequest = partial(
    HttpError, status=499, message="Client closed request"
)

# Errors with codes 5XX
InternalServerError = partial(
    HttpError, status=500, message="Internal server error"
)
NotImplementedHTTP = partial(HttpError, status=501, message="Not implemented")
BadGateway = partial(HttpError, status=502, message="Bad gateway")
ServiceUnavailable = partial(
    HttpError, status=503, message="Service unavailable"
)
GatewayTimeout = partial(HttpError, status=504, message="Gateway timeout")
HTTPVersionNotSupported = partial(
    HttpError, status=505, message="HTTP version not supported"
)
VariantAlsoNegotiates = partial(
    HttpError, status=506, message="Variant also negotiates"
)
InsufficientStorage = partial(
    HttpError, status=507, message="Insufficient storage"
)
LoopDetected = partial(HttpError, status=508, message="Loop detected")
BandwidthLimitExceeded = partial(
    HttpError, status=509, message="Bandwidth limit exceeded"
)
NotExtended = partial(HttpError, status=510, message="Not extended")
NetworkAuthenticationRequired = partial(
    HttpError, status=511, message="Network authentication required"
)
UnknownError = partial(
    HttpError, status=520, message="Unknown error"
)
WebServerIsDown = partial(
    HttpError, status=521, message="Web server is down"
)
ConnectionTimedOut = partial(
    HttpError, status=522, message="Connection timed out"
)
OriginIsUnreachable = partial(
    HttpError, status=523, message="Origin is unreachable"
)
ATimeoutOccurred = partial(
    HttpError, status=524, message="A timeout occurred"
)
