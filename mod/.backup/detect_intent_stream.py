#!/usr/bin/env python

# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""DialogFlow API Detect Intent Python sample with audio files processed
as an audio stream.

Examples:
  python detect_intent_stream.py -h
  python detect_intent_stream.py --project-id PROJECT_ID \
  --session-id SESSION_ID --audio-file-path resources/book_a_room.wav
  python detect_intent_stream.py --project-id PROJECT_ID \
  --session-id SESSION_ID --audio-file-path resources/mountain_view.wav
"""

# [START import_libraries]
import argparse
import uuid
import os
import json
import aiy.i18n
import aiy.audio
from six.moves import queue

import dialogflow
# [END import_libraries]

credentials_file = os.path.expanduser('~/cloud_speech.json')
_detect_intent_stream = None

class Audio_Stream(object):
    def __init__(self):
        self._audio_queue = queue.Queue()

    def reset(self):
        while True:
            try:
                self._audio_queue.get(False)
            except queue.Empty:
                return

    def add_data(self, data):
        self._audio_queue.put(data)

    def end_audio(self):
        self.add_data(None)

    def request_stream(self, audio_config, session):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        yield dialogflow.types.StreamingDetectIntentRequest(
                session=session, query_input=query_input)

        while True:
            data = self._audio_queue.get()

            if not data:
                return

            yield dialogflow.types.StreamingDetectIntentRequest(
                input_audio=data)

class _Detect_Intent_Stream(object):

    def __init__(self, credentials_file):

        self._recorder = aiy.audio.get_recorder()

        self.language_code = aiy.i18n.get_language_code()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        self.project_id = format(json.load(open(credentials_file))['project_id'])

        self.audio_stream = Audio_Stream()

    # [START dialogflow_detect_intent_streaming]
    def recognize(self, session_id):
        """Returns the result of detect intent with streaming audio as input.

        Using the same `session_id` between requests allows continuation
        of the conversaion."""
        session_client = dialogflow.SessionsClient()

        # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
        audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
        sample_rate_hertz = 16000

        session = session_client.session_path(self.project_id, session_id)
        print('Session path: {}\n'.format(session))

        self.audio_stream.reset()
        self._recorder.add_processor(self.audio_stream)

        audio_config = dialogflow.types.InputAudioConfig(
            audio_encoding=audio_encoding, language_code=self.language_code,
            sample_rate_hertz=sample_rate_hertz)

        requests = self.audio_stream.request_stream(audio_config, session)
        responses = session_client.streaming_detect_intent(requests)

        print('=' * 20)

        for response in responses:
            print('Intermediate transcript: "{}".'.format(
                    response.recognition_result.transcript))
            print('is_final?: "{}".'.format(
                    response.recognition_result.is_final))
            if response.recognition_result.is_final == True:
                    self._recorder.remove_processor(self.audio_stream)
                    self.audio_stream.end_audio()

        # Note: The result from the last response is the final transcript along
        # with the detected content.
        query_result = response.query_result

        print('=' * 20)
        print('Query text: {}'.format(query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            query_result.intent.display_name,
            query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            query_result.fulfillment_text))
        return query_result.fulfillment_text
        # [END dialogflow_detect_intent_streaming]

def get_recognizer():
    global _detect_intent_stream
    if not _detect_intent_stream:
        _detect_intent_stream = _Detect_Intent_Stream(credentials_file)
    return _detect_intent_stream


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project-id',
        help='Project/agent id.  Required.')
    parser.add_argument(
        '--session-id',
        help='Identifier of the DetectIntent session. '
        'Defaults to a random UUID.',
        default=str(uuid.uuid4()))
    parser.add_argument(
        '--language-code',
        help='Language code of the query. Defaults to "en-US".')
    parser.add_argument(
        '--audio-file-path',
        help='Path to the audio file.')

    args = parser.parse_args()
    aiy.audio.get_recorder().start()

    req = _Detect_Intent_Stream(credentials_file)

    req.recognize(args.session_id)
