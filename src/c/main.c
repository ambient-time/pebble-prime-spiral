// Copyright 2026 Luke Steuber. MIT License.
#include <pebble.h>
#include "prime.h"
#include "digits.h"
static Window *s_window;
static Layer *s_layer;
static bool s_focused;
static uint32_t s_frames;
static AppTimer *s_timer;
static int s_burst_frames,s_last_second=-1;
static void disc(GContext *ctx,GPoint p,int radius,GColor color){
  graphics_context_set_fill_color(ctx,color);graphics_fill_circle(ctx,p,radius);
}
static void draw(Layer *layer,GContext *ctx){
  time_t epoch;uint16_t millis;time_ms(&epoch,&millis);struct tm local=*localtime(&epoch);
  PrimeTime time=prime_time(local.tm_hour,local.tm_min,local.tm_sec,s_burst_frames?millis:0);
  GRect bounds=layer_get_bounds(layer);int w=bounds.size.w,h=bounds.size.h;
  int radius=(w<h?w:h)*435/1000;GPoint center=GPoint(w/2,h/2);
  graphics_context_set_antialiased(ctx,true);graphics_context_set_fill_color(ctx,GColorBlack);
  graphics_fill_rect(ctx,bounds,0,GCornerNone);
  unsigned active=0;
  for(int i=0;i<1799;i++){
    const PrimeDot *dot=&PRIME_DOTS[i];uint8_t v=prime_intensity(dot,time);
    GPoint p=GPoint(center.x+dot->x*radius/16384,center.y+dot->y*radius/16384);
    if(dot->prime){
      int size=1+(v*3+127)/255;
      if(v>40){
        active++;
#ifdef PBL_COLOR
        disc(ctx,p,size+2,GColorDarkGray);disc(ctx,p,size+1,GColorLightGray);
#endif
      }
#ifdef PBL_COLOR
      disc(ctx,p,size,v>40?GColorWhite:GColorLightGray);
#else
      disc(ctx,p,size,GColorWhite);
#endif
    }else if(v>81){
#ifdef PBL_COLOR
      disc(ctx,p,1,GColorDarkGray);
#else
      if(i%4==0)disc(ctx,p,0,GColorWhite);
#endif
    }
  }
  // The source supplies this compact center readout for small displays.
  int panel=w>=240?32:w>=180?28:25;
  disc(ctx,center,panel+2,GColorBlack);
  graphics_context_set_stroke_color(ctx,PBL_IF_COLOR_ELSE(GColorDarkGray,GColorWhite));
  graphics_context_set_stroke_width(ctx,1);graphics_draw_circle(ctx,center,panel);
  char text[6];prime_readout(text,local.tm_hour,local.tm_min);
  draw_digits(ctx,text,center.x,center.y,w>=240?2:1,GColorWhite);
  s_frames++;
  if(s_last_second!=local.tm_sec){
    uint16_t end;time_ms(NULL,&end);
    APP_LOG(APP_LOG_LEVEL_INFO,"Prime time=%02d:%02d:%02d.%03d active=%u ms=%d heap=%lu frames=%lu",
      local.tm_hour,local.tm_min,local.tm_sec,millis,active,(end+1000-millis)%1000,
      (unsigned long)heap_bytes_free(),(unsigned long)s_frames);
    s_last_second=local.tm_sec;
  }
}
static void cancel_timer(void){if(s_timer){app_timer_cancel(s_timer);s_timer=NULL;}}
static void animate(void *context){s_timer=NULL;if(!s_focused||!s_burst_frames)return;
  s_burst_frames--;layer_mark_dirty(s_layer);if(s_burst_frames)s_timer=app_timer_register(125,animate,NULL);}
static void burst(void){cancel_timer();if(!s_focused)return;s_burst_frames=48;
  layer_mark_dirty(s_layer);s_timer=app_timer_register(125,animate,NULL);}
static void tick(struct tm *t,TimeUnits changed){if(s_focused&&!s_burst_frames)layer_mark_dirty(s_layer);}
static void tap(AccelAxisType axis,int32_t direction){burst();}
static void focus(bool focused){s_focused=focused;if(focused)layer_mark_dirty(s_layer);else{cancel_timer();s_burst_frames=0;}}
static void load(Window *window){s_layer=layer_create(layer_get_bounds(window_get_root_layer(window)));
  layer_set_update_proc(s_layer,draw);layer_add_child(window_get_root_layer(window),s_layer);}
static void unload(Window *window){cancel_timer();layer_destroy(s_layer);s_layer=NULL;}
static void init(void){s_window=window_create();window_set_background_color(s_window,GColorBlack);
  window_set_window_handlers(s_window,(WindowHandlers){.load=load,.unload=unload});window_stack_push(s_window,false);
  tick_timer_service_subscribe(SECOND_UNIT,tick);accel_tap_service_subscribe(tap);app_focus_service_subscribe(focus);focus(true);}
static void deinit(void){s_focused=false;cancel_timer();tick_timer_service_unsubscribe();accel_tap_service_unsubscribe();app_focus_service_unsubscribe();window_destroy(s_window);}
int main(void){init();app_event_loop();deinit();}
