select cDNA ,count(SampleNumber)as EpisodeCount
from Occurrence
group by cDNA;

