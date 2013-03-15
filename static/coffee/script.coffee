# context = new AudioContext()
# request = new XMLHttpRequest()
# request.open('GET', '#', true)
# request.responseType = 'arraybuffer';
# request.addEventListender('load', () ->
#     context.decodeAudioData(request.response, (buffer) -> 
#         source = context.createBufferSource();
#         Array.prototype.reverse.call(buffer.getChannelData(0) )
#         Array.prototype.reverse.call( buffer.getChannelData(1) )
#         source.buffer = buffer
#         source.loop = false;
#         source.connect(context.destination)
#         source.noteOn(0) 
#         )
#     )

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
    reader.onload = (e) -> init_sound(this.result)
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