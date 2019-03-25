/*========================================================================
 * extract_cols_from_sbet.c
 *
 * Derived from:
 * 2011-02-15  Bruce Raup  braup@nsidc.org
 * National Snow & Ice Data Center, University of Colorado, Boulder
 *
 * Convert binary SBET file from Applanix to human readable CSV.
 * Only X, Y, Z, Roll, Pitch, and Heading are extracted.
 * The output file is later used with pandas to query geo-location according to
 * GPS time.
 *
 * Compile with:
 *  gcc -o extract_cols_from_sbet extract_cols_from_sbet.c
 *========================================================================*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define SLASH "/"
#define to_degrees(radians) (( radians * (180.0 / M_PI) ))

typedef struct {
  double time;
  double lat;       // in radians
  double lon;       // in radians
  double alt;
  double x_vel;
  double y_vel;
  double z_vel;
  double roll;      // in radians
  double pitch;     // in radians
  double heading;   // in radians
  double wander;
  double x_force;
  double y_force;
  double z_force;
  double x_ang_rate;
  double y_ang_rate;
  double z_ang_rate;
} record_type;

int main(int argc, char **argv) {
  FILE *infile, *outfile;
  record_type rec;

  size_t sz;
  int num_items;
  int outfile_path_length;
  const char outfile_name[9] = "sbet.csv";

  sz = sizeof(record_type);

  infile = fopen(argv[1], "rb");
  if (! infile) {
    fprintf(stderr, "Can't open %s for reading\n", argv[1]);
    exit(1);
  }

  if (! argv[2]) {
    fprintf(stderr, "Missing output file path\n");
    exit(1);
  }

  outfile_path_length = strlen(outfile_name) + 1 + strlen(argv[2]);
  char outfile_path[outfile_path_length];
  strcpy(outfile_path, argv[2]);

  char *last_from_path = &argv[2][strlen(argv[2]) - 1];
  if (strncmp(last_from_path, SLASH, 1) > 1) {
    strcat(outfile_path, SLASH);
  }

  strcat(outfile_path, outfile_name);

  outfile = fopen(outfile_path, "w");
  if (! outfile) {
    fprintf(stderr, "Can't open %s for reading\n", argv[2]);
    exit(1);
  }

  fprintf(stderr, "Writing output file:\n  %s\n", outfile_path);

  fprintf(outfile, "GpsTime,X,Y,Z,Heading,Roll,Pitch\n");

  while (1) {
    num_items = fread(&rec, sz, 1, infile);

    if (num_items != 1) {
      break;
    }

    fprintf(outfile,
            "%lf,%lf,%lf,%lf,%lf,%lf,%lf\n",
            rec.time,
            to_degrees(rec.lon),
            to_degrees(rec.lat),
            rec.alt,
            to_degrees(rec.heading),
            to_degrees(rec.roll),
            to_degrees(rec.pitch)
    );
  }

  fclose(infile);
  fclose(outfile);
}

