import sys

import musicbrainz as m

def main():
	#print m.get_artist_by_id("952a4205-023d-4235-897c-6fdb6f58dfaa", [])
	#print m.get_label_by_id("aab2e720-bdd2-4565-afc2-460743585f16")
	#print m.get_release_by_id("e94757ff-2655-4690-b369-4012beba6114")
	#print m.get_release_group_by_id("9377d65d-ffd5-35d6-b64d-43f86ef9188d")
	#print m.get_recording_by_id("cb4d4d70-930c-4d1a-a157-776de18be66a")
	print m.get_work_by_id("7e48685c-72dd-3a8b-9274-4777efb2aa75")

if __name__ == "__main__":
	main()
