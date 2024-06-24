import json
DefHeader = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2ZXJfdHMiOjE3MTkyMTAwNzU3MDgsInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsidm5mbSJdLCJkb21haW5zIjpbeyJuYW1lIjoiY2RzMiIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIl19LHsibmFtZSI6ImVkZ2UiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfSx7Im5hbWUiOiJmaXNfd2hxIiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiLCJvd25lciJdfSx7Im5hbWUiOiJvcDEyMyIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3AyMyIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3AyMzMiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciIsIm93bmVyIl19LHsibmFtZSI6Im9wNDAiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfSx7Im5hbWUiOiJvcDQ1Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoib3A2NiIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3BlbnN0YWNrMjMiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciIsIm93bmVyIl19LHsibmFtZSI6Im9wXzQ1Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoidGVuYW50Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoidXNlciIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIl19LHsibmFtZSI6InZuZm0iLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfV0sImV4cCI6MTcxOTIxMDA5NSwiYXV0aG9yaXRpZXMiOlsiYWRtaW4iXSwianRpIjoic1l4UzJLYVFsSDNVanRnYVlBTlpCel9IZ2UwIiwiY2xpZW50X2lkIjoidm5mbSJ9.PIq1H_TaYYnBr6DfwbcDRIdQSQ97PpgD0YiLJgCsOUA",
    "token_type": "bearer",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2ZXJfdHMiOjE3MTkyMTAwNzU3MDgsInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsidm5mbSJdLCJhdGkiOiJzWXhTMkthUWxIM1VqdGdhWUFOWkJ6X0hnZTAiLCJkb21haW5zIjpbeyJuYW1lIjoiY2RzMiIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIl19LHsibmFtZSI6ImVkZ2UiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfSx7Im5hbWUiOiJmaXNfd2hxIiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiLCJvd25lciJdfSx7Im5hbWUiOiJvcDEyMyIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3AyMyIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3AyMzMiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciIsIm93bmVyIl19LHsibmFtZSI6Im9wNDAiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfSx7Im5hbWUiOiJvcDQ1Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoib3A2NiIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIiwib3duZXIiXX0seyJuYW1lIjoib3BlbnN0YWNrMjMiLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciIsIm93bmVyIl19LHsibmFtZSI6Im9wXzQ1Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoidGVuYW50Iiwicm9sZXMiOlsiYWRtaW4iLCJtZW1iZXIiXX0seyJuYW1lIjoidXNlciIsInJvbGVzIjpbImFkbWluIiwibWVtYmVyIl19LHsibmFtZSI6InZuZm0iLCJyb2xlcyI6WyJhZG1pbiIsIm1lbWJlciJdfV0sImV4cCI6MTcxOTI1MzI3NSwiYXV0aG9yaXRpZXMiOlsiYWRtaW4iXSwianRpIjoiSlRwQVAwQkdhajlrekZmX1luVGxIc3NvanZjIiwiY2xpZW50X2lkIjoidm5mbSJ9.ju7CuymF8ozKck08LFFmy1JqhXXxsbgeDRTAVxgrgSk",
    "expires_in": 19,
    "scope": "vnfm",
    "server_ts": 1719210075708,
    "domains": [
        {
            "name": "cds2",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "edge",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "fis_whq",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "op123",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "op23",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "op233",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "op40",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "op45",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "op66",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "openstack23",
            "roles": [
                "admin",
                "member",
                "owner"
            ]
        },
        {
            "name": "op_45",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "tenant",
            "roles": [
                "admin",
                'member'
            ]
        },
        {
            "name": "user",
            "roles": [
                "admin",
                "member"
            ]
        },
        {
            "name": "vnfm",
            "roles": [
                "admin",
                "member"
            ]
        }
    ],
    "jti": "sYxS2KaQlH3UjtgaYANZBz_Hge0"
}

print(type(DefHeader))