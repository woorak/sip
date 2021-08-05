import sip
import media
import time
import sys
import server


def test_server():
    params={'alias':'alias1',
             'rh':'172.30.3.155',
            'rp':5060,
            'lh':'10.1.230.24',
            'lp':5060,
            'transport':'tcp',
            }
    server.run(params)
    
def test_re_invite():
    params={'alias':'alias1',
            'rh':'172.30.3.155',
            'rp':5060,
            'lh':'10.1.195.25',
            'lp':5060,
            'transport':'tcp',
            }
     
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    sip.send_ack(params)
    print('in call...')
    time.sleep(1)
    sip.send_re_invite(params, sip.sdp2(params))
    res = sip.get_invite_response(params)
    sip.send_ack(params)
    if (res[0] == 200):
        sdp = res[2]
        p = media.gst(media.parse_sdp(sdp))
        time.sleep(30)
    p.kill()
    sip.send_bye(params)
    time.sleep(1)

def test_call_media(params, duration):
   
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    sip.send_ack(params)
    print('in call...')
    sdp = res[2]
    p = media.gst(media.parse_sdp(sdp))
    for t in range(duration):
        time.sleep(1)
        tick()
    p.kill()
    sip.send_bye(params)
    time.sleep(1)

def tick():
    sys.stdout.write('.')
    
def test_call2():
    params={'alias':'alias1',
            'rh':'10.1.195.217',
            'rp':5060,
            'lh':'10.1.195.25',
            'lp':5060,
            'transport':'tcp',
            }
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    sip.send_ack(params)
    print('in call...')
    time.sleep(10)
    sip.send_bye(params)
    time.sleep(1)
    
    
    
test_server()

# params={'alias':'alias1',
#             'rh':'10.1.195.214',
#             'rp':5060,
#             'lh':'10.1.195.247',
#             'lp':5060,
#             'transport':'tcp',
#             }
# for test in range (100):
#     print('==================== test=========={}'.format(test))
#     test_call_media(params, 10)
#     time.sleep(2)
