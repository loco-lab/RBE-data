Data for the Radio Background Experiment (RBE) on the DORA cubesat.

The DORA heartbeat telemetry includes satellite and payload health status and various other telemetry and payload data variables. For full list of variables, see here:

Each full heartbeat was separated into 2 packets, after the "payload_filter_bank_power_ch2" variable. Heartbeats were transmitted on 2-GFSK modulation scheme. The full list of observations can be found on the SatNOGS database for DORA: https://db.satnogs.org/satellite/QZRL-4914-4557-2700-9931.

After demodulating, hex data can be decoded with https://github.com/DylanL7/dora-data. This decodes the first and second half packets separately, and adds "observation_time", "altitude", "lat", "long" to both packets, and an additional "timestamp" to the second half packet. The output from the decoder are the heartbeat_firsthalf.csv and heartbeat_secondhalf.csv files in this repo.

Additional data processing with RBEanalysis.py matches the first half to the second half and throws out unmatched packet halves, any packets before the deployement of the RBE antenna, and any repeated or unupdated packets. The final RBE data can be found in RBEhearbeat.csv. Plotting of this data can also be found in RBEanalysis.py.
