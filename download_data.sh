while IFS=,
  read youtube_video_id width height frame_rate ; do
  FILE=${youtube_video_id}
  if [ ! -f "$FILE".* ]; then
  echo "$FILE"
    youtube-dl --o ${youtube_video_id} \
    https://www.youtube.com/watch?v=${youtube_video_id} ;
  fi
done < missing_data.txt
