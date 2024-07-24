from django.shortcuts import render
from django.conf import settings



def kakao_login(request):
    auth_url = settings.KAKAO_AUTH_URL
    client_id = settings.KAKAO_CLIENT_ID
    redirect_uri = settings.KAKAO_REDIRECT_URL

    kakao_auth_url = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(kakao_auth_url)

def kakao_callback(request):
    code = request.GET.get('code')
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_CLIENT_ID,
        'redirect_uri': settings.KAKAO_REDIRECT_URL,
        'code': code,
        'client_secret': settings.KAKAO_CLIENT_SECRET,
    }
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    token_response = request.post(settings.KAKAO_TOKEN_URL, data=token_data, headers=token_headers)

    if token_response.status_code != status.HTTP_200_OK:
        return HttpResponse(
            f"카카오 토큰 받기 실패 💀 {token_response.content}",
            status=500,
        )

    access_token = token_response.json().get('access_token')

    profile_response = request.get(
        settings.KAKAO_PROFILE_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    )
    profile_info = profile_response.json()

    print(json.dumps(profile_info))

    response = HttpResponse(user_profile, status=status.HTTP_200_OK)

    return response


def kakao_logout(request):
    logout(request)
    return redirect(settings.KAKAO_LOGOUT_URL)


