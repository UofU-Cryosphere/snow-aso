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
#define OUTPUT_FILE "sbet.csv"

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

void checkFileAccess(FILE *file, char *argv) {
  if (! file) {
    fprintf(stderr, "Can't open %s for reading\n", argv);
    exit(1);
  }
}

void checkPathArgument(char *argv, int number) {
  if (! argv) {
    if (number == 1) {
      fprintf(stderr, "Missing input file path\n");
    } else if (number == 2) {
      fprintf(stderr, "Missing output file path\n");
    }
    exit(1);
  }
}

// Ensure a trailing slash for the output path
void ensureSlash(char *output_path, char *argv) {
  char *last_from_path = &argv[strlen(argv) - 1];

  if (strcmp(last_from_path, SLASH) != 0) {
    strcat(output_path, SLASH);
  }
  strcat(output_path, OUTPUT_FILE);
}

void writeFile(FILE *infile, FILE *outfile) {
  record_type rec;
  size_t sz = sizeof(record_type);
  int num_items;

  fprintf(outfile, "GpsTime,X,Y,Z,Heading,Roll,Pitch\n");

  while ((num_items = fread(&rec, sz, 1, infile))) {
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
}

int main(int argc, char **argv) {
  FILE *infile, *outfile;

  int outfile_path_length;

  checkPathArgument(argv[1], 1);
  infile = fopen(argv[1], "rb");
  checkFileAccess(infile, argv[1]);

  checkPathArgument(argv[2], 2);

  outfile_path_length = strlen(argv[2]) + 1 + strlen(OUTPUT_FILE);
  char outfile_path[outfile_path_length];
  strcpy(outfile_path, argv[2]);
  ensureSlash(outfile_path, argv[2]);

  outfile = fopen(outfile_path, "w");
  checkFileAccess(outfile, argv[2]);

  printf("Writing output file:\n  %s\n", outfile_path);
  writeFile(infile, outfile);

  fclose(infile);
  fclose(outfile);
}

