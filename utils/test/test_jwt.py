import sys
import anfler.util.jwt.jwt_helper as jwtw

if __name__ == '__main__':
    JWT_CONFIG = {
        "PRIVATE_KEY":None,
        "PRIVATE_KEY_FILE":"private.pem.txt",
        "PRIVATE_PASS": "dusEZzcDqhSAIJeY",
        "PUBLIC_KEY_FILE": "public.pem.txt",
        "ALGORITHM": "RS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": 5
    }
    jwtw.jwt_set_config(JWT_CONFIG)
    print("JWT_CONFIG", jwtw.JWT_CONFIG)

    data = {"username":"anfler"}
    print("Data1:", data)
    token = jwtw.jwt_encode(data)
    print("Token1:", token)
    print("Decoded data1:" , jwtw.jwt_decode(token))


    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpYXQiOjE2MTQ3ODQxNjIsImV4cCI6MTYxNDc5MTM2Miwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoia2V2aW50ZXJ1ZWwzNDVAZ21haWwuY29tIiwiaWQiOjd9.LzX6il0TYAF1Ifh5Nn_qW6vJy9sbaeiE44tiMKpg0UrlTodCUp8yPewRE_kzKwpF45Jf3wqfGZsY_w6asHh7wjElnLS-LFf7cAOG9qtPLQctZNI5He9wcK7fwH0XRSWhgoRqzm2nxgNSkH0KhYtAUC-_HbUfQtqtu-tqEXtqEBO1Lm_OCTU_6JlEVGiHnp9X2JTrjpZ9iJeBLakYRSodZJxiVNmD7Atr4CPO5eVg9haYT-5B_YGbCqK3_XvafEeVB5QohxegJm1kH5UCmJ115f4iqoQdS5iAdWzlrJe5Ya5sKoNiDU9JrXpwrum3r_Onj6_OPl0PqSrUiH72VayXKHoore48HkDnhdoKyLzieZDum3ATgIbWcHwxF_C8WACjyWMqgkGyeaadfDHLT31_8OFO-wuOiKf0Grds-eolNepqBgU02HogD9UYnOISyc4ZWxJzd9M7KKfG5oatOT_uHMjsIUqMvUCc7pad3flc9X-ww7y6Ni5ZQx6ZhRFj8WF4TC8FXeQUu_mhprKNYGNJLMA3yYvgTG0HcLnC0zAx3cqgq96aMNi03g1vp7VYoMFw1V0wvvfKkHDV1zLTwUhLtCZccHVIH2oIWAzIUrl8gmHOlOHkIRp1rZc2Xs9RAYiZmmnIC9t0Ssz6KgtHz6_e77jUILDv4g456OaISwOFFYg"
    print("Token2:", token)
    print("Decoded data2:", jwtw.jwt_decode(token))


