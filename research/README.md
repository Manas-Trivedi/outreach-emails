# Research Internship Outreach

Cold-outreach to **faculty** at IITs, NITs, and IIITs for research internships.
Separate from the `industry/` track (HR / company recruiting) because the data
shape and the pitch are different: here we target professors by **research area**,
not companies by hiring need.

## Layout: institute type → state → city → institute

```
faculty/
├── iits/   <state>/<city>/<institute>.csv
├── nits/   <state>/<city>/<institute>.csv
└── iiits/  <state>/<city>/<institute>.csv
```

Example: `faculty/iits/maharashtra/mumbai/iit-bombay.csv`

- **`faculty_master.csv`** — every faculty row merged + deduped. Single source of
  truth that the batch generator reads from.
- **`batches/`** — `research_batch_NN.csv`, 100 contacts each, ready for mail-merge.
- **`dead_removed.csv`** — bounced / retired / opted-out contacts, pruned from the pool.

## CSV schema (identical in every file)

```
name,state,city,institute,institute_type,department,email,research_area,personal_site,priority,status,notes
```

| column          | notes                                                        |
|-----------------|-------------------------------------------------------------|
| institute_type  | `IIT` \| `NIT` \| `IIIT`                                     |
| research_area   | short tag(s), e.g. `computer-vision;3d-tracking`            |
| priority        | `1` (top target) … `3`                                       |
| status          | `queued / sent / follow-up-1 / replied / accepted / rejected / no-response` |

Because `state`, `city`, and `institute_type` are **columns** (not only folders),
the master CSV can be grouped any way at generate time — by state, by city, or by
institute family — without duplicating rows.

## Templates

Live in `../templates/`: `research_cold.md`, `follow_up_1.md`, `follow_up_2.md`.
