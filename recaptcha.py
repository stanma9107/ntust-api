from anticaptchaofficial.recaptchav2proxyless import *

def recaptchaSolver(apiKey, url, siteKey):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(apiKey)
    solver.set_website_url(url)
    solver.set_website_key(siteKey)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        return {
            "success": True,
            "result": g_response
        }
    else:
        return {
            "success": False
        }