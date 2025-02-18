Data for the Radio Background Experiment (RBE) on the DORA cubesat.

The DORA heartbeat telemetry includes satellite and RBE payload health status and various other telemetry and payload data variables. A full explanation of the RBE payload telemetry can be found in the [DORA Payload Manual]{https://docs.google.com/document/d/1KkSb6C9l4m5digKVfBHimGuwScWpahmjAZQ6TM97j2k/edit?tab=t.0}.

Each full heartbeat was separated into 2 packets, after the "payload_filter_bank_power_ch2" variable. Heartbeats were transmitted on 2-GFSK modulation scheme. The full list of observations can be found on the SatNOGS database for DORA: https://db.satnogs.org/satellite/QZRL-4914-4557-2700-9931. Instructions for demodulating data from the SatNOGS database can be found in DemodulatingDORAdata.pdf.

After demodulating, hex data can be decoded with the [DORA decoder]{https://github.com/DylanL7/dora-data}. This decodes the first and second half packets separately, and adds "observation_time", "altitude", "lat", "long" to both packets, and an additional "timestamp" to the second half packet. The output from the decoder are the heartbeat_firsthalf.csv and heartbeat_secondhalf.csv files in this repo.

Additional data processing with RBEanalysis.py matches the first half to the second half and throws out unmatched packet halves, any packets before the deployement of the RBE antenna, and any repeated or unupdated packets. The final RBE data can be found in RBEhearbeat.csv. Plotting of this data can also be found in RBEanalysis.py.

Associated publications:

Zhao, Y., Jacobs, D. C., Samson, T., Bowman, J., and Lalonde, M.-O. R. Building a global map of low frequency radio interference from orbit with DORA. Radio Science, RFI 2024 Special Edition. [in press, expected Mar 2025.]{https://doi.org/10.22541/essoar.173884449.96853776/v1}

Zhao, Y., Jacobs, D. C., Bowman, J., Samson, T. and Lalonde, M.-O. R. Pathfinding Low Frequency Radio Astronomy with the DORA Radio Background Experiment. 2025 IEEE Aerospace Conference Proceedings. in press, expected Mar 2025.
