/* -*- c++ -*- */
/*
 * Copyright 2008,2009,2013,2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

#ifndef INCLUDED_GR_WAVFILE_SINK_IMPL_H
#define INCLUDED_GR_WAVFILE_SINK_IMPL_H

#include <gnuradio/blocks/wavfile.h>
#include <gnuradio/blocks/wavfile_sink.h>
#include <sndfile.h> // for SNDFILE

namespace gr {
namespace blocks {

class wavfile_sink_impl : public wavfile_sink
{
private:
    wav_header_info d_h;
    int d_bytes_per_sample_new;
    bool d_append;

    float d_max_sample_val;
    float d_min_sample_val;
    float d_normalize_shift;
    float d_normalize_fac;

    SNDFILE* d_fp;
    SNDFILE* d_new_fp;
    bool d_updated;
    boost::mutex d_mutex;

    /*!
     * \brief If any file changes have occurred, update now. This is called
     * internally by work() and thus doesn't usually need to be called by
     * hand.
     */
    void do_update();

    /*!
     * \brief Implementation of set_bits_per_sample without mutex lock.
     */
    void set_bits_per_sample_unlocked(int bits_per_sample);

    /*!
     * \brief Writes information to the WAV header which is not available
     * a-priori (chunk size etc.) and closes the file. Not thread-safe and
     * assumes d_fp is a valid file pointer, should thus only be called by
     * other methods.
     */
    void close_wav();

protected:
    bool stop();

public:
    wavfile_sink_impl(const char* filename,
                      int n_channels,
                      unsigned int sample_rate,
                      wavfile_format_t format,
                      wavfile_subformat_t subformat,
                      bool append);
    ~wavfile_sink_impl();

    bool open(const char* filename);
    void close();

    void set_sample_rate(unsigned int sample_rate);
    void set_bits_per_sample(int bits_per_sample);
    void set_append(bool append) override;

    int bits_per_sample();
    unsigned int sample_rate();

    int work(int noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star& output_items);
};

} /* namespace blocks */
} /* namespace gr */

#endif /* INCLUDED_GR_WAVFILE_SINK_IMPL_H */
