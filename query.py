import sys

import musicbrainzngs as m

def main():
	m.set_useragent("application", "0.01", "http://example.com")
	print m.get_artist_by_id("952a4205-023d-4235-897c-6fdb6f58dfaa", [])
	#print m.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16")
	#print m.get_release_by_id("e94757ff-2655-4690-b369-4012beba6114")
	#print m.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
	#print m.get_recording_by_id("cb4d4d70-930c-4d1a-a157-776de18be66a")
	#print m.get_work_by_id("7e48685c-72dd-3a8b-9274-4777efb2aa75")

	#print m.get_releases_by_discid("BG.iuI50.qn1DOBAWIk8fUYoeHM-")
	#print m.get_recordings_by_puid("070359fc-8219-e62b-7bfd-5a01e742b490")
	#print m.get_recordings_by_isrc("GBAYE9300106")

	m.auth("", "")
	#m.submit_barcodes({"e94757ff-2655-4690-b369-4012beba6114": "9421021463277"})
	#m.submit_puids({"cb4d4d70-930c-4d1a-a157-776de18be66a":"e94757ff-2655-4690-b369-4012beba6114"})
	#m.submit_tags(recording_tags={"cb4d4d70-930c-4d1a-a157-776de18be66a":["these", "are", "my", "tags"]})
	#m.submit_tags(artist_tags={"952a4205-023d-4235-897c-6fdb6f58dfaa":["NZ", "twee"]})

	#m.submit_ratings(recording_ratings={"cb4d4d70-930c-4d1a-a157-776de18be66a":20})

	#print m.get_recordings_by_echoprint("aryw4bx1187b98dde8")
    #m.submit_echoprints({"e97f805a-ab48-4c52-855e-07049142113d": "anechoprint1234567"})

if __name__ == "__main__":
	main()
