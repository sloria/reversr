###
RECORDING
###

RECORDING_LIMIT = 10 * 1000
timecode = (ms) ->
    hms = 
        h: Math.floor( ms / (60*60*1000) ),
        m: Math.floor( (ms/60000) % 60 ),
        s: Math.floor( ms/1000 % 60 )
    
    tc = []
    tc.push(hms.h) if hms.h > 0

    tc.push( 
        if hms.m < 10 and hms.h > 0 then "0" + hms.m else hms.m
    )

    tc.push(
        if hms.s < 10 then "0" + hms.s else hms.s
    )
    return tc.join(':')

Recorder.initialize({
    swfSrc: "/static/libs/recorder/recorder.swf"
})

record = () ->
    Recorder.record({
        start: () -> 
            document.getElementById('record_button').disabled = true
            document.getElementById("stop_button").disabled = false 
        progress: (milliseconds) ->
            document.getElementById("time").innerHTML = timecode(milliseconds)
            if milliseconds > RECORDING_LIMIT
                Recorder.stop()
        cancel: () ->
            document.getElementById('record_button').disabled = false 
            document.getElementById("stop_button").disabled = true
    })

play = () ->
    Recorder.stop()
    Recorder.play({
        progress: (milliseconds) ->
            document.getElementById('time').innerHTML = timecode(milliseconds)
        finished: () -> 
    })

stop = () -> 
    document.getElementById('record_button').disabled = false 
    document.getElementById("stop_button").disabled = true
    Recorder.stop()
    upload()

upload = () ->
   Recorder.upload({
      url: "/",
      audioParam: "audio_file",
      success: (response) ->
        window.n_channels = 1
        track = $.parseJSON(response)
        load_sound_file(track.filepath)
   })

$('#record_button').click () -> record()
$('#play_button').click () -> play()
$('#stop_button').click () -> stop()
$('#upload_button').click () -> upload()

file_input = document.querySelector('input[type="file"]')
file_input.addEventListener('change', (e) ->
    reader = new FileReader()
    reader.onload = (e) ->
        window.n_channels = 2
        init_sound(this.result)
    reader.readAsArrayBuffer(this.files[0])
, false)

$('#play_reversed').click () -> 
    stop_sound
    play_reversed()
$('#stop_sound').click () -> stop_sound()


