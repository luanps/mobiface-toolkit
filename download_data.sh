while IFS=,
  read name youtube_video_id width height frame_rate first_frame last_frame; do
   ./youtube-dl -o ${name} https://www.youtube.com/watch?v=${youtube_video_id}
   -width  ${width} -height  ${height} -fps ${frame_rate};
done < videolist.csv
