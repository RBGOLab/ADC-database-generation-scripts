SELECT
	up.Accession, # uniprot accession code
	en.ENSEMBL_Gene_Id, # Gene id from ENSEMBL
	en.GeneName, # Name of Genes

	CAST(up.TM_CellMembraneYN AS UNSIGNED) AS LocCellMemUniprot, # located in cell membrane from uniprot
	CAST(up.SecretedYN AS UNSIGNED) AS Secreted,
	up.Length,

	tis.TissueName, # cancer tissuename
	ctl.Antigen_HPA_Id, # Human protein atlas antigen Id
	ROUND(100*ctl.LevelHighF/(ctl.LevelLowF + ctl.LevelNotDetectedF + ctl.LevelHighF + ctl.LevelMediumF),2) AS perHigh,
	ROUND(100*ctl.LevelMediumF/(ctl.LevelLowF + ctl.LevelNotDetectedF + ctl.LevelHighF + ctl.LevelMediumF),2) AS perMedium,
	ROUND(100*ctl.LevelLowF/(ctl.LevelLowF + ctl.LevelNotDetectedF + ctl.LevelHighF + ctl.LevelMediumF),2) AS perLow,
	ROUND(100*ctl.LevelNotDetectedF/(ctl.LevelLowF + ctl.LevelNotDetectedF + ctl.LevelHighF + ctl.LevelMediumF),2) AS perNotDetected,
	ctl.LevelLowF + ctl.LevelNotDetectedF + ctl.LevelHighF + ctl.LevelMediumF AS totalF, # total female patients
	hts.ovary, # expression level in healthy ovary
	hts.endometrium1, # expression level in healthy endometrium1

	(tm.TopconsTM_N>0) + (tm.OctopusTM_N>0) + (tm.SpoctopusTM_N>0) + (tm.PhiliusTM_N>0) + (tm.ScampiTM_N>0) + (tm.PolyPhobiusTM_N>0) AS NumberTMPreds, # number of TM tools predict TM region
	tm.ShortestO, # shortest predicted outer region
	tm.LongestO, # Longest predicted outer region
	LEAST(tm.TopconsTM_N,tm.OctopusTM_N,tm.SpoctopusTM_N,tm.PhiliusTM_N,tm.ScampiTM_N,tm.PolyPhobiusTM_N) AS LowestNoTMregions,
	GREATEST(tm.TopconsTM_N,tm.OctopusTM_N,tm.SpoctopusTM_N,tm.PhiliusTM_N,tm.ScampiTM_N,tm.PolyPhobiusTM_N) AS HighestNoTMregions,
	#AVG(tm.TopconsTM_N,tm.OctopusTM_N,tm.SpoctopusTM_N,tm.PhiliusTM_N,tm.ScampiTM_N,tm.PolyPhobiusTM_N) AS MeanNoTMregions,
	ex.Existence # add this after - cell membrane

	FROM
		tmpredsummary tm USE INDEX (TMN_LongOutDx)
		JOIN
			uniprot_proteins up USE INDEX (tmRegsCelMemExistDx)
			ON up.Id = tm.UniprotId
				JOIN
					uniprotensembljunc uej
					ON up.Accession = uej.UniProt_Accession
						JOIN
							ensembl_genes en USE INDEX (ensmblIdGeneNm)
							ON uej.ENSEMBL_Gene_Id = en.Ensembl_Gene_Id
								JOIN
									healthytissuelevelsrows_hpa hts USE INDEX (enIdOvEnd1Dx)
									ON en.Ensembl_Gene_Id = hts.ENSEMBL_Gene_Id
									JOIN
										cancertissuelevel_hpa ctl USE INDEX (tisLevAllDx)
										ON en.Ensembl_Gene_Id = ctl.ENSEMBL_Gene_Id
											JOIN
												cancertissue_hpa tis
												ON ctl.CancTissue_Id = tis.Id
													JOIN
														proteinevidence_up ex
															ON up.ExistenceId = ex.Id


		WHERE
			tis.TissueName LIKE 'ovarian cancer' AND
			((hts.ovary LIKE 'not detected' OR hts.ovary LIKE 'low') AND
			(hts.endometrium1 LIKE 'not detected' OR hts.endometrium1 LIKE 'low' OR hts.endometrium1 IS NULL))
		ORDER BY NumberTMPreds DESC #, perHigh DESC, perMedium DESC, up.TM_CellMembraneYN DESC
		INTO OUTFILE 'ovarianCancerProteins.txt'
		;
