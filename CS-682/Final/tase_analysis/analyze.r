library(readr)
library(ggplot2)

audio_with_text <- read_csv("~/Documents/tase_analysis/benchmark1_audio-with-text.csv", na="empty")
text_with_audio <- read_csv("~/Documents/tase_analysis/benchmark1_text-with-audio.csv", na="empty")

# AUDIO WITH TEXT

audio_with_text -> normalized_data
normalized_data <- normalized_data[1:9]
normalized_data$confidence <- replace(normalized_data$confidence, normalized_data$returned_word_position == -1, 0)
normalized_data$distance <- replace(abs(normalized_data$distance), abs(normalized_data$distance) > 10, 10)
#nd <- subset(normalized_data, normalized_data$distance < 3)
#nd2 <- data.frame(mean(nd$clip_movement*nd$clip_size),mean(nd$distance))
#colnames(nd2) <- c("x","y")
normalized_data <- subset(normalized_data, normalized_data$match_percent >= 0.7)
ggplot(data = normalized_data, aes(x=clip_size*clip_movement, y=distance, color=factor(match_percent))) +geom_point(size=2, aes(alpha=confidence)) +stat_ellipse(data = subset(normalized_data, normalized_data$distance < 3),type="t", level=0.02, geom="path", size=0.8, linetype=1) +geom_smooth(method="lm", level=0.2) +ggtitle("Distance (in words) vs. Clip Factor") +xlab("Clip Factor (clip size * clip movement)") +ylab("Distance (lower is better)") +labs(color="Match Percent", alpha="Confidence", subtitle="Audio with Text Synchronization") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20))
ggsave("~/Documents/tase_analysis/AwT-distance_vs_clip_factor.png", device="png", width=20, height=15, units="cm")
ggplot(data = subset(normalized_data, confidence >= 0.5), aes(x=confidence, y=distance, color=distance < 5)) +geom_point() +stat_ellipse(type="t", level=0.9, linetype=1) +ggtitle("Distance (in words) vs. Confidence") +xlab("Confidence") +ylab("Distance (lower is better)") +labs(color="Acceptable\nDistance", subtitle="Audio with Text Synchronization") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20)) +geom_hline(yintercept=5, linetype=2) +scale_y_continuous(breaks=c(0,2,4,6,8,10))
ggsave("~/Documents/tase_analysis/AwT-distance_vs_confidence.png", device="png", width=20, height=15, units="cm")
ggplot(data=subset(normalized_data, distance < 5), aes(x=clip_size*clip_movement, y=sync_time, color=factor(match_percent))) +geom_point() +geom_smooth(level=0.1) +ggtitle("Sync Time vs. Clip Factor") +xlab("Clip Factor") +ylab("Sync Time (s)") +labs(subtitle="Audio with Text Synchronization", color="Match Percent") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20)) +geom_vline(xintercept=50, linetype=2) +geom_vline(xintercept=90, linetype=2) +geom_rect(xmin=50, xmax=90, ymin=0, ymax=10, fill="yellow", alpha=0.002, linetype=0)
ggsave("~/Documents/tase_analysis/AwT-sync_time_vs_clip_factor.png", device="png", width=20, height=15, units="cm")


# TEXT WITH AUDIO

text_with_audio -> normalized_data
normalized_data <- normalized_data[1:9]
normalized_data$confidence <- replace(normalized_data$confidence, normalized_data$returned_audio_timestamp == -1, 0)
normalized_data$distance <- replace(abs(normalized_data$distance), abs(normalized_data$distance) > 10000, 10000) #distance in milliseconds
normalized_data <- subset(normalized_data, normalized_data$match_percent >= 0.7)
ggplot(data = normalized_data, aes(x=clip_size*clip_movement, y=distance, color=factor(match_percent))) +geom_point(size=2, aes(alpha=confidence)) +stat_ellipse(data = subset(normalized_data, normalized_data$distance < 3000),type="t", level=0.02, geom="path", size=0.8, linetype=1) +geom_smooth(method="lm", level=0.2) +ggtitle("Distance vs. Clip Factor") +xlab("Clip Factor (clip size * clip movement)") +ylab("Distance in ms (lower is better)") +labs(color="Match Percent", alpha="Confidence", subtitle="Text with Audio Synchronization") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20))
ggsave("~/Documents/tase_analysis/TwA-distance_vs_clip_factor.png", device="png", width=20, height=15, units="cm")
ggplot(data = subset(normalized_data, confidence >= 0.5), aes(x=confidence, y=distance, color=distance < 5000)) +geom_point() +stat_ellipse(type="t", level=0.9, linetype=1) +ggtitle("Distance vs. Confidence") +xlab("Confidence") +ylab("Distance in ms (lower is better)") +labs(color="Acceptable\nDistance", subtitle="Text with Audio Synchronization") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20)) +geom_hline(yintercept=4000, linetype=2) #+scale_y_continuous(breaks=c(0,2,4,6,8,10))
ggsave("~/Documents/tase_analysis/TwA-distance_vs_confidence.png", device="png", width=20, height=15, units="cm")
ggplot(data=subset(normalized_data, distance < 5000), aes(x=clip_size*clip_movement, y=sync_time, color=factor(match_percent))) +geom_point() +geom_smooth(level=0.1) +ggtitle("Sync Time vs. Clip Factor") +xlab("Clip Factor") +ylab("Sync Time (s)") +labs(subtitle="Text with Audio Synchronization", color="Match Percent") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20)) +geom_vline(xintercept=90, linetype=2) +geom_vline(xintercept=150, linetype=2) +geom_rect(xmin=90, xmax=150, ymin=-10, ymax=10000, fill="yellow", alpha=0.002, linetype=0)
ggsave("~/Documents/tase_analysis/TwA-sync_time_vs_clip_factor.png", device="png", width=20, height=15, units="cm")

# OVERALL

text_with_audio_clean <- text_with_audio
text_with_audio_clean$confidence <- replace(text_with_audio_clean$confidence, text_with_audio_clean$returned_audio_timestamp == -1, 0)
text_with_audio_clean$distance <- replace(abs(text_with_audio_clean$distance), abs(text_with_audio_clean$distance) > 10000, 10000)
text_with_audio_clean <- subset(text_with_audio_clean, distance < 5000)
audio_with_text_clean <- audio_with_text
audio_with_text_clean$confidence <- replace(audio_with_text_clean$confidence, audio_with_text_clean$returned_word_position == -1, 0)
audio_with_text_clean$distance <- replace(abs(audio_with_text_clean$distance), abs(audio_with_text_clean$distance) > 10, 10)
audio_with_text_clean <- subset(audio_with_text_clean, distance < 5)
df1 <- cbind(text_with_audio_clean[1:3], text_with_audio_clean[8:9], rep("Text -> Audio", each=length(text_with_audio_clean$clip_size)))
colnames(df1) <- c("clip_size", "match_percent", "clip_movement", "confidence", "sync_time", "conv_type")
df2 <- cbind(audio_with_text_clean[1:3], audio_with_text_clean[8:9], rep("Audio -> Text", each=length(audio_with_text_clean$clip_size)))
colnames(df2) <- c("clip_size", "match_percent", "clip_movement", "confidence", "sync_time", "conv_type")
normalized_data <- rbind(df1, df2)

ggplot(data=normalized_data, aes(x=clip_size*clip_movement, y=sync_time, color=factor(conv_type))) +geom_point() +geom_smooth(linetype=1) +ggtitle("Sync Time vs. Clip Factor") +xlab("Clip Factor") +ylab("Sync Time (s)") +labs(subtitle="Both Synchronization Directions", color="Direction") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20)) +scale_y_continuous(trans="log10") +geom_vline(xintercept=90, linetype=2) +geom_vline(xintercept=150, linetype=2) +geom_rect(xmin=90, xmax=150, ymin=-10, ymax=10000, fill="green", alpha=0.002, linetype=0) +geom_vline(xintercept=50, linetype=2) +geom_rect(xmin=50, xmax=90, ymin=-10, ymax=10000, fill="yellow", alpha=0.002, linetype=0)
ggsave("~/Documents/tase_analysis/both-sync_time_vs_clip_factor.png", device="png", width=20, height=15, units="cm")

# OPTIMALS

audio_with_text_optimal <- read_csv("~/Documents/tase_analysis/benchmark2_audio-with-text.csv", na="empty")
#audio_with_text_optimal$returned_word_position <- replace(audio_with_text_optimal$returned_word_position, audio_with_text_optimal$returned_word_position == -1, 0)
audio_with_text_optimal$confidence <- replace(audio_with_text_optimal$confidence, audio_with_text_optimal$returned_word_position == -1, 0)
ggplot(data=audio_with_text_optimal, aes(x=sync_time, color=returned_word_position == -1)) +stat_ecdf(geom="step", size=1) +ggtitle("CDF of Sync Time - Optimal Parameters") +xlab("Sync Time (s)") +ylab("Fraction of Trials") +labs(subtitle="Audio with Text Synchronization", color="Convergence") +theme_linedraw() +theme(axis.text.x = element_text(size=16), axis.title.x = element_text(size=20), axis.title.y = element_text(size=20), axis.text.y=element_text(size=16), legend.text = element_text(size=16), legend.title=element_text(size=20), title=element_text(size=20))
ggsave("~/Documents/tase_analysis/AwT-CDF-sync-time.png", device="png", width=20, height=15, units="cm")
