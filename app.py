import streamlit as st
import yt_dlp

# Função para pegar os formatos do vídeo
def get_formats(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        format_list = [{"id": f["format_id"], "resolution": f.get('height', 'N/A'), "codec": f.get('vcodec', 'N/A')} for f in formats]
        return format_list

# Função para baixar o vídeo
def download_video(url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Interface do Streamlit
st.title("Vidloader - Baixar Vídeos")
st.write("Digite a URL do vídeo e escolha o formato desejado.")

# Input para a URL
video_url = st.text_input("URL do Vídeo")

if video_url:
    # Pega os formatos do vídeo
    formats = get_formats(video_url)

    if formats:
        st.write("Escolha a qualidade e formato:")
        # Lista os formatos disponíveis
        format_options = [f"{f['resolution']}p - {f['codec']}" for f in formats]
        selected_format = st.selectbox("Escolha o formato", format_options)

        # Botão para download
        if st.button("Baixar Vídeo"):
            # Encontra o formato escolhido
            chosen_format = formats[format_options.index(selected_format)]
            download_video(video_url, chosen_format['id'])
            st.success("Download iniciado!")
    else:
        st.error("Não foi possível obter os formatos do vídeo.")
