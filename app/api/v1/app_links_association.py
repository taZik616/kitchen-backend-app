from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def AppleAppSiteAssociationView(request):
    return Response({
        "applinks": {
            "apps": [],
            "details": [
                {
                    # "<TeamID>.<BundleId>"
                    "appIDs": ["<TeamID>.<BundleId>"],
                    "paths": ["*"]
                }
            ]
        },
        "webcredentials": {
            "apps": ["<TeamID>.<BundleId>"]
        },
    })


@api_view(['GET'])
def AndroidAppSiteAssociationView(request):
    return Response([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "package_name",
            "sha256_cert_fingerprints":
            ["00:00"]
        }
    }])
