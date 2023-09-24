import sys
import os
import json
import glob
import struct
import base64

def check_audio_files(file_list):
    error_list = []
    for file_name in file_list:
        file_info = {'file_name': file_name, 'error_type': []}
        
        # 파일 존재 여부 확인
        if not os.path.exists(file_name):
            file_info['error_type'].append('파일이 존재하지 않음')
            error_list.append(file_name)
            continue
        
        try:
            with open(file_name, 'rb') as file:
                # WAV 파일 헤더 정보 확인
                header = file.read(44)
                if len(header) != 44 or header[:4] != b'RIFF':
                    file_info['error_type'].append('헤더만 존재함')
                    error_list.append(file_name)
                
                # 데이터 값 확인
                else:
                    data = file.read()
                    if not data:
                        file_info['error_type'].append('데이터 값이 없음')
                        error_list.append(file_name)
        
        except Exception as e:
            file_info['error_type'].append('클리핑 에러')
            error_list.append(file_name)
    
    return error_list

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 Q2.py <입력 파일 경로> <출력 파일 경로>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # 'pcmlist.txt' 파일에서 경로를 읽어와서 WAV 파일 경로를 glob으로 가져옴
    with open(input_file, 'r', encoding='utf-8') as pcm_file:
        pcm_paths = [line.strip() for line in pcm_file]

    # 'pcmlist.txt' 파일에 나열된 WAV 파일 경로를 glob으로 확장
    wav_list = []
    for pcm_path in pcm_paths:
        wav_list.extend(glob.glob(pcm_path))

    # 가져온 WAV 파일 경로를 출력
    print("다음 WAV 파일들이 불러와졌습니다:")
    for file_path in wav_list:
        print(file_path)

    # WAV 파일 오류 검출
    error_list = check_audio_files(wav_list)

    # 결과를 딕셔너리로 저장
    result_dict = {"error_list": error_list}

    # 결과를 JSON 파일에 저장
    with open(output_file, "w", encoding='utf-8') as json_file:
        json.dump(result_dict, json_file, indent=2)

    print(f'오류가 검출된 파일은 {output_file}에 저장되었습니다.')