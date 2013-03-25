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
        start: () -> console.log 'Started recording'
        progress: (milliseconds) -> 
            document.getElementById("time").innerHTML = timecode(milliseconds)
            Recorder.stop() if milliseconds > RECORDING_LIMIT

    })

play = () ->
    Recorder.stop()
    Recorder.play({
        progress: (milliseconds) ->
            document.getElementById('time').innerHTML = timecode(milliseconds)
        finished: () -> 
            console.log Recorder.audioData()
    })

stop = () -> 
    Recorder.stop()
    # init_sound(Recorder.audioData)
    play()

$('#record_button').click ()-> record()
$('#play_button').click () -> play()
$('#stop_button').click () -> stop()

### REVERSING ###

context = new window.webkitAudioContext()
source = null
audio_buffer = null

stop_sound = () -> source.noteOff(0) if source

play_sound = () ->
    source = context.createBufferSource()
    Array.prototype.reverse.call( audio_buffer.getChannelData(0) )
    Array.prototype.reverse.call( audio_buffer.getChannelData(1) )
    source.buffer = audio_buffer
    source.loop = false
    source.connect(context.destination)
    source.noteOn(0) # Play


init_sound = (array_buffer) ->
    context.decodeAudioData(array_buffer, (buffer) -> 
        audio_buffer = buffer
        buttons = document.querySelectorAll('button')
        buttons[0].disabled = false
    , (e) -> console.log('Error decoding file', e)
    )

file_input = document.querySelector('input[type="file"]')
file_input.addEventListener('change', (e) ->
    reader = new FileReader()
    reader.onload = (e) -> 
        console.log this.result
        init_sound(this.result)
    reader.readAsArrayBuffer(this.files[0])
, false)

load_sound_file = (url) ->
    xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.onload = (e) -> init_sound(this.response)
    xhr.send()

window.stop_sound = stop_sound
window.play_sound = play_sound
window.load_sound_file = load_sound_file


