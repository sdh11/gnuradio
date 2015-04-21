/* -*- c++ -*- */
/*
 * Copyright 2005-2011 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include "tag_delay_impl.h"
#include <stdio.h>
#include <gnuradio/io_signature.h>
#include <boost/thread/thread.hpp>

namespace gr {
  namespace blocks {

    tag_delay::sptr
    tag_delay::make(size_t itemsize, int delay)
    {
      return gnuradio::get_initial_sptr
        (new tag_delay_impl(itemsize, delay));
    }

    tag_delay_impl::tag_delay_impl(size_t itemsize,
                                   int delay)
      : sync_block("tag_delay",
                      io_signature::make(1, 1, itemsize),
                      io_signature::make(1, 1, itemsize)),
        d_itemsize(itemsize),
        d_sleep(false)
    {
      if (delay < 0) {
        throw std::runtime_error("tag delay: Cannot initialize block with a delay < 0.");
      }
      d_delay = delay;
    }

    tag_delay_impl::~tag_delay_impl()
    {
    }

    int
    tag_delay_impl::work(int noutput_items,
                        gr_vector_const_void_star &input_items,
                        gr_vector_void_star &output_items)
    {
      if (d_sleep) {
        boost::this_thread::sleep(boost::posix_time::milliseconds(d_delay));
        d_sleep = false;
      }

      const char *in = (const char *)input_items[0];
      char *out = (char *)output_items[0];

      // Get all the input tags
      std::vector<tag_t> tags;
      get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0) + noutput_items);

      if (tags.size() > 0) {
        unsigned long offset = tags[0].offset - nitems_read(0);
        //printf("Tag offset - %lu\n", tags[0].offset);
        //printf("items read %lu\n", nitems_read(0));
        //printf("offset = %lu\n", offset);

        // Check the location and number of tags
        if (offset > 0) {
          //printf("Offset > 0; Sending %d items\n", offset);
          // Number of tags doesn't matter. Only send up to the first tag
          std::memcpy(out, in, offset * d_itemsize);
          d_sleep = true;
          return offset;
        } else if (offset == 0 && tags.size() == 1) {
          //printf("Tag is aligned to 0. Single tag. Sending %d items\n", noutput_items);
          // This is the only tag and it's aligned, which means it was delayed.
          // Send everything.
          std::memcpy(out, in, noutput_items * d_itemsize);
          return noutput_items;
        } else {
          // Tag is aligned, but there are more than one in the buffer.
          // Send everything until the next tag, then sleep.
          offset = tags[1].offset - nitems_read(0);
          //printf("Tag is aligned, but more than one tag. Sending %d items\n", offset);
          std::memcpy(out, in, offset * d_itemsize);
          d_sleep = true;
          return offset;
        }
      } else {
        std::memcpy(out, in, noutput_items * d_itemsize);
        return noutput_items;
      }
    }

  } /* namespace blocks */
} /* namespace gr */
