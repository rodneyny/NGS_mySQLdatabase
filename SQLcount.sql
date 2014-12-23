select T.Refseq, COUNT(V.cDNA) As NumberOfVariants
from Variants V
inner join Transcripts T
on V.Refseq=T.Refseq
group by T.Refseq
;