import sip
import transport
import time


def handle(params, message):
   
    res = sip.parse_message(message)
    headers = res[0]
    header = headers[0]
    sip.log_sip_recv(params, headers[0])
    
    if 'INVITE' in header:
        #sdp = res[2]
        #p = media.gst(media.parse_sdp(sdp))
        sdp = sip.response_sdp(params)
        ir =  sip.create_invite_response(params, headers, sdp)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)
        return ir
    
    elif 'UPDATE' in header:
        ir =  sip.create_update_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)
        return ir
    elif 'ACK' in header:
        time.sleep(1)
        ir = sip.create_re_invite(params, sip.response_sdp2(params))
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)
        return ir
    elif 'Trying' in header:
        return ''
    elif '200 OK' in header:
        ir = sip.create_ack(params)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)
        return ir
    
    elif 'BYE' in header:
        ir =  sip.create_bye_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)
        return ir
    
    elif 'REGISTER' in header:
        trying =  sip.create_100_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(trying)[0]))
        sip.log_sip_send(params, trying)

        ir =  sip.create_register_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        sip.log_sip_send(params, ir)

        return (trying, ir)
        
    else:
        raise RuntimeError("{}  ...not implemented yet.".format(header))

def run(params):
    
    transport.server(params, handle)
    
    
    