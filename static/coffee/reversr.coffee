### Reverse Playback ###
context = new window.webkitAudioContext()
source = null
audio_buffer = null

window.n_channels = 2

stop_sound = () -> source.noteOff(0) if source

play_reversed = () ->
    source = context.createBufferSource()
    Array.prototype.reverse.call( audio_buffer.getChannelData(0) )
    Array.prototype.reverse.call( audio_buffer.getChannelData(1) ) if window.n_channels > 1
    source.buffer = audio_buffer
    source.loop = false
    source.connect(context.destination)
    source.noteOn(0) # Play

play_sound = () ->
    source = context.createBufferSource()
    source.buffer = audio_buffer
    source.loop = true
    source.connect(context.destination)
    source.noteOn(0) # Play

init_sound = (array_buffer) ->
    context.decodeAudioData(array_buffer, (buffer) -> 
        audio_buffer = buffer
        buttons = document.querySelectorAll('button')
        buttons[0].disabled = false
    , (e) -> console.log('Error decoding file', e)
    )


load_sound_file = (url) ->
    request = new XMLHttpRequest()
    request.open('GET', url, true)
    request.responseType = 'arraybuffer'
    request.onload = (e) -> init_sound(this.response)
    request.send()



window.stop_sound = stop_sound
window.play_sound = play_sound
window.play_reversed = play_reversed
window.init_sound = init_sound
window.load_sound_file = load_sound_file

