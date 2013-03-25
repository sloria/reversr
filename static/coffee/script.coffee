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
